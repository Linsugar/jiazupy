# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

class Bucket_Handle():  #存储桶操作
    def __init__(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        secret_id = 'AKIDPZYIn4luQnuoVCnq9KGyRuHPGuJmvzjD'  # 替换为用户的 secretId
        secret_key = 'OVQ7vUnpcvWrwl13qOaaKZgYCoCLEsOi'  # 替换为用户的 secretKey
        region = 'ap-chengdu'  # 替换为用户的 Region
        token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        # proxies = {
        #     'http': '127.0.0.1:80',  # 替换为用户的 HTTP代理地址
        #     'https': '127.0.0.1:443'  # 替换为用户的 HTTPS代理地址
        # }
        endpoint = 'cos.accelerate.myqcloud.com'
        scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region,Endpoint=endpoint,SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        self.client = CosS3Client(config)

    def Create_Bucket(self,BucketName):
        # 创建存储桶名字
        BucketNmae=self.client.create_bucket(Bucket=BucketName)
        return BucketNmae

    def Serach_Bucket(self):
        # 查询存储桶列表
        print(self.client.list_buckets())
        return self.client.list_buckets()

    def Upload_File(self,filename = 'picture.jpg',filepath= './images/name1.jpg'):
        self.client.upload_file(
            Bucket='tazh-1257606718',
            LocalFilePath=filepath,
            Key=filename,
            PartSize=1,
            MAXThread=10,
            EnableMD5=False
        )
        print('返回图片地址：'+'https://tazh-1257606718.cos.ap-chengdu.myqcloud.com/'+filename)
        return 'https://tazh-1257606718.cos.ap-chengdu.myqcloud.com/'+filename

if __name__ == '__main__':
    Result = Bucket_Handle()
    Result.Upload_File()