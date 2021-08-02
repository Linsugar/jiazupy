# import hashlib
# # import random
# # import time
# # import requests
# # import json
# # app_key = 'p5tvi9dsplrv4'
# # nonce = random.randint(10000800, 121023151000)
# # tm = int(time.time())
# # allstr = 'DiVY2bK9iwhZG' + str(nonce) + str(tm)
# # sha = hashlib.sha1(allstr.encode('utf-8')).hexdigest()
# # url = 'https://api-cn.ronghub.com/user/getToken.json'
# # headers ={
# #     "App-Key": app_key,
# #     "Nonce": str(nonce),
# #     "Timestamp": str(tm),
# #     "Signature": sha,
# # }
# #
# # data = {
# #     'userId':'ysjs12122',
# #     'name':"测试3",
# #     'portraitUri':'http://qr0n4nltx.hn-bkt.clouddn.com/1618567483851351.jpg'
# # }
# # result = requests.post(url=url,data=data,headers=headers)
# # print(result.status_code)
# # rs = json.loads(result.text)
# # # print(rs['token'])
#
#
# inputValue = input("请输入内容：")
#
# print(type(inputValue))
# # 判断是否全字母符串
# res  = inputValue.isalpha()
# #判断是否
# print(res)

# import json
#
# data = [
# 'xx','xxx','22'
# ]
# v = "['xxx','xxx2','xxxx1']"
# s = eval(v)
# print(s)
# print(type(s))
# print(eval(v))
# k = ["xxx","xxx2","xxxx1"]
#
# json_data = json.dumps(k )
# print(json_data)
import locale

from datetime import datetime


# locale.setlocale(locale.LC_CTYPE, 'chinese')
stime = datetime.now()
s = stime.strftime('%Y-%m-%d %H:%M:%S')
print(s)
