# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
import sys
import logging
import time
from qiniu import Auth, put_file, etag
class Bucket_Handle():  #存储桶操作
    def __init__(self):
        access_key = 'cyIcJU0RXy1nD1t0I6DauqqCblEcFX1npjtld5Ky'
        secret_key = 'Vt7Yw39U3COUnW1uavsLMRpPiSCtQ8mdJ0Hl2vmK'
        self.q = Auth(access_key=access_key,secret_key=secret_key)
    #
    # def Create_Bucket(self,BucketName):
    #     # 创建存储桶名字
    #     BucketNmae=self.client.create_bucket(Bucket=BucketName)
    #     return BucketNmae
    #
    # def Serach_Bucket(self):
    #     # 查询存储桶列表
    #     print(self.client.list_buckets())
    #     return self.client.list_buckets()

    def upToken(self):
        bucket_name = "tanghuadong"
        # 3600为token过期时间，秒为单位。3600等于一小时
        token =self.q.upload_token(bucket_name)
        print(token)
        return token
if __name__ == '__main__':
    Result = Bucket_Handle()