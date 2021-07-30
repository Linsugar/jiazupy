import locale
import time
import hashlib
from datetime import datetime
locale.setlocale(locale.LC_CTYPE, 'chinese')
class Power(object):
    def Power_Md5(self,user):
        m5 = hashlib.md5()
        m5.update(bytes(str(user),encoding='utf-8'))
        print('当前时间：'+str(time.time()))
        m5.update(bytes(str(time.time()),encoding='utf-8'))
        print("加密内容："+ m5.hexdigest())
        return m5.hexdigest()

class GetLocalTime(object):
    def __init__(self):
        self.NowTime = datetime.now()
#     获取本地时间
    def GetTimeYearTime(self):
#     //年月日 时分秒
        Ytime = self.NowTime.strftime('%Y年%m月%d日 %H:%M:%S')
        return Ytime


if __name__ == '__main__':
    Power().Power_Md5("6666")