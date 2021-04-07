import time
import hashlib

class Power(object):
    def Power_Md5(self,user):
        m5 = hashlib.md5()
        m5.update(bytes(str(user),encoding='utf-8'))
        print('当前时间：'+str(time.time()))
        m5.update(bytes(str(time.time()),encoding='utf-8'))
        print("加密内容："+ m5.hexdigest())
        return m5.hexdigest()
if __name__ == '__main__':
    Power().Power_Md5("6666")