import hashlib
import json
import random
import time
import requests

class rongyun():

    def __init__(self):
        self.app_key = 'p5tvi9dsplrv4'
        self.nonce = random.randint(10000800, 121023151000)
        self.tm = int(time.time())
        self.app_scrent = 'DiVY2bK9iwhZG'
        self.allstr =self.app_scrent+ str(self.nonce) + str(self.tm)
        self.sha = hashlib.sha1(self.allstr.encode('utf-8')).hexdigest()
        self.url = 'https://api-cn.ronghub.com/user/getToken.json'
        self.headers ={
            "App-Key": self.app_key,
            "Nonce": str(self.nonce),
            "Timestamp": str(self.tm),
            "Signature": self.sha,
        }

    def register_roog(self,user_id,name=None,portraitUri=None):
        data = {
            'userId':user_id,
            'name':name,
            'portraitUri': portraitUri
        }
        result = requests.post(url=self.url, data=data,headers=self.headers)
        rs = json.loads(result.text)
        return rs
