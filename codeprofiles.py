from requests_html import HTMLSession
import json
import requests
import requests
from bs4 import BeautifulSoup
class UsernameError(Exception):
    pass
class PlatformError(Exception):
    pass

class User:
    def __init__(self,username=None,platform=None):
        self.__username = username
        self.__platform = platform
    def codechef(self):
        url = "https://codechef.com/users/{}".format(self.__username)
        session = HTMLSession()
        d = dict()
        r = session.get(url,timeout=10)
        d['username']=self.__username
        if r.status_code!=200:
            raise UsernameError("User not found")
        try:
            rating_header = r.html.find(".rating-header",first=True)
        except:
            raise UsernameError('User not found')

        try:
            rating = rating_header.find(".rating-number",first=True).text
            d["rating"]=rating
        except:
            raise UsernameError('User not found')
        max_rating = rating_header.find('small')[0].text[1:-1].split()[2]
        rating_star = len(r.html.find(".rating-star",first=True).find('span'))
        ranks = r.html.find('.rating-ranks',first=True).find('strong')
        global_rank = ranks[0].text
        country_rank = ranks[1].text
        d["global_rank"]=global_rank
        d["country_rank"]=country_rank
        return d
       
      
                
    def codeforces(self):
        url = 'https://codeforces.com/api/user.info?handles={}'.format(self.__username)
        r = requests.get(url,timeout=10)
        if r.status_code !=200:
            raise UsernameError('User not found')
        r_data = r.json()
        if r_data['status']!='OK':
            raise UsernameError('User not found')
        d  = dict()
        d['username']=self.__username
        d['ranking']=r_data['result'][0]['rank']
        d['maxRating']=r_data['result'][0]['maxRating']           
        return d
    def gfg(self):
        url = "https://auth.geeksforgeeks.org/user/{}/?utm_source=geeksforgeeks".format(self.__username)
        response = requests.get(url)
        if response.status_code == 200:
           soup = BeautifulSoup(response.text, 'html.parser')
        d = dict()
        data = list()
        d['username']=self.__username   
        d['institute_rank']=soup.select('.rankNum')[0].text
        d['total_no_of_problems']=soup.select('.score_card_value')[1].text
        d['coding_score']=soup.select('.score_card_value')[0].text
        # data.append(d)
        return d
           
           
        
        
        
    def leetcode(self):
        
        url="https://leetcode-stats-api.herokuapp.com/{}".format(self.__username)
        r = requests.get(url)
        if r.status_code !=200:
            raise UsernameError('User not found')
        r_data = r.json()
        d=dict()
        d['username']=self.__username
        d['totalSolved']=r_data["totalSolved"]
        d['ranking']=r_data["ranking"]
        d['acceptanceRate']=r_data["acceptanceRate"]
        return d
    def github(self):
        url=" https://api.github.com/users/{}".format(self.__username)
        r=requests.get(url)
        if r.status_code !=200:
            raise UsernameError('User not found')
        r_data = r.json()
        url1="https://api.github.com/users/{}/repos".format(self.__username)
        r1=requests.get(url1)
        if r1.status_code !=200:
            raise UsernameError('User not found')
        r1_data = r1.json()
        d=dict()
        dr=dict()
        d['username']=r_data["login"]
        d['public_repos']=r_data["public_repos"]
        l=len(r1_data)
        for i in range(l):
            li=[]
            li.append(r1_data[i]["name"])
            li.append(r1_data[i]["html_url"])
            dr["repo{}".format(i)]=li
        return dr
        
        
       
        
           
    def get_info(self):
        if self.__platform=='codechef':
            return self.codechef()
        if self.__platform=='codeforces':
            return self.codeforces()
        if self.__platform =='leetcode':
            return self.leetcode()
        if self.__platform =='gfg':
            return self.gfg()
        if self.__platform =='github':
            return self.github()
        raise PlatformError('Platform not Found')
    

        
        
    
if __name__ == '__main__':
    platform = input("Enter platform: ")
    username = input("Enter username: ")
    obj = User(username,platform)
    print(obj.get_info())
   
    
    
 