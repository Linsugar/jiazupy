import hashlib
import random
import time
import requests
import json
app_key = 'p5tvi9dsplrv4'
nonce = random.randint(10000800, 121023151000)
tm = int(time.time())
allstr = 'DiVY2bK9iwhZG' + str(nonce) + str(tm)
sha = hashlib.sha1(allstr.encode('utf-8')).hexdigest()
url = 'https://api-cn.ronghub.com/user/getToken.json'
headers ={
    "App-Key": app_key,
    "Nonce": str(nonce),
    "Timestamp": str(tm),
    "Signature": sha,
}

data = {
    'userId':'ysjs12122',
    'name':"测试3",
    'portraitUri':'http://qr0n4nltx.hn-bkt.clouddn.com/1618567483851351.jpg'
}
result = requests.post(url=url,data=data,headers=headers)
print(result.status_code)
rs = json.loads(result.text)
print(rs['token'])