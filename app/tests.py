# # import hashlib
# # # import random
# # # import time
# # # import requests
# # # import json



v1 = [1,2,3]
v2 = [4,5,6]
v3 = v1+v2
print(v3)
# # # app_key = 'p5tvi9dsplrv4'
# # # nonce = random.randint(10000800, 121023151000)
# # # tm = int(time.time())
# # # allstr = 'DiVY2bK9iwhZG' + str(nonce) + str(tm)
# # # sha = hashlib.sha1(allstr.encode('utf-8')).hexdigest()
# # # url = 'https://api-cn.ronghub.com/user/getToken.json'
# # # headers ={
# # #     "App-Key": app_key,
# # #     "Nonce": str(nonce),
# # #     "Timestamp": str(tm),
# # #     "Signature": sha,
# # # }
# # #
# # # data = {
# # #     'userId':'ysjs12122',
# # #     'name':"测试3",
# # #     'portraitUri':'http://qr0n4nltx.hn-bkt.clouddn.com/1618567483851351.jpg'
# # # }
# # # result = requests.post(url=url,data=data,headers=headers)
# # # print(result.status_code)
# # # rs = json.loads(result.text)
# # # # print(rs['token'])
# #
# #
# # inputValue = input("请输入内容：")
# #
# # print(type(inputValue))
# # # 判断是否全字母符串
# # res  = inputValue.isalpha()
# # #判断是否
# # print(res)
#
# # import json
# #
# # data = [
# # 'xx','xxx','22'
# # ]
# # v = "['xxx','xxx2','xxxx1']"
# # s = eval(v)
# # print(s)
# # print(type(s))
# # print(eval(v))
# # k = ["xxx","xxx2","xxxx1"]
# #
# # json_data = json.dumps(k )
# # print(json_data)
# import locale
#
# from datetime import datetime
#
#
# # locale.setlocale(locale.LC_CTYPE, 'chinese')
# # stime = datetime.now()
# # s = stime.strftime('%Y-%m-%d %H:%M:%S')
# # print(s)
# # print(len("https://thirdwx.qlogo.cn/mmopen/vi_32/AH3uEYUVGPdxgMic6eCAx8LJdibgx0Z2gVeJO5yOhZ3VsLqdtxue2egPsdlmtSw0uBh63hazibChicvdtnUIPQlS6w/132"))
#
#
# a = 1628588558093
#
# aflterTime = datetime.now().timestamp()+24*60*60
# noteTime = datetime.now().timestamp()
# print(noteTime)
# print(aflterTime>noteTime)

import redis

# import redis
#
# red = redis.StrictRedis(host='139.155.88.241',port=6379,db=0)
# red.flushdb()
# for i in range(0,6):
#     red.rpush('list', i)
# print(red.lrange('list',0,-1))
# print(red.llen('list'))
# print(red.mset(
#    {
#         'v1':1,
#         'v2':3
#     }
# ))
# print(red.exists('v1'))
# print(red.exists('v1'))
# print(red.append('v1','tang'))
# # red.hmset('test',{
# #     'm':1,
# #     't':2
# # })
# red.hset('uk','ui',2)
# print(red.hget('uk','ui'))
# # red.expire('uk','1000')
# print(red.pttl('uk'))



# value0 = input("请输入男用户等级：")
# value1 = input("请输入女用户等级：")
#
# x1 = eval(value0)/10
# print("男值："+str(x1))
# if x1 < 3:
#     y = 1
# else:
#     y = 0
# print("男最终亲密值："+str(x1+y))
# x2 = eval(value1)/10
# print("女值："+str(x2))
# if x2 < 3:
#     y = 8
# else:
#     y = 10
# print("女最终亲密值："+str(x2+y))
