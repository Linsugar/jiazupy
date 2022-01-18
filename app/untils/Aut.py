import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication,jwt_decode_handler
import time

VISIT_RECORD = {}
# 自定义限制,访问频率
class MyThrottle(object):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        """
        自定义频率限制60秒内只能访问三次
        """
        # 获取用户IP
        ip = request.META.get("REMOTE_ADDR")
        print(f'ip={ip}')
        timestamp = time.time()
        if ip not in VISIT_RECORD:
            VISIT_RECORD[ip] = [timestamp, ]
            return True
        history = VISIT_RECORD[ip]
        self.history = history
        history.insert(0, timestamp)
        print(history)
        while history and history[-1] < timestamp - 60:
            history.pop()
        if len(history) > 3:
            return False
        else:
            return True

    def wait(self):
        """
        限制时间还剩多少
        """
        timestamp = time.time()
        return 60 - (timestamp - self.history[-1])



#自定义jwt认证
class Jwt_Authentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        print(request.method)
        # if request.method.lower()=='post':
        #     return ('','')
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value =request.META.get('HTTP_AUTHORIZATION')
        if jwt_value is None:
            raise AuthenticationFailed('非法用户')
        token = self.leng_jwt(jwt_value)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('已过期')
        except jwt.DecodeError:
            raise AuthenticationFailed('非法用户')

        user = self.authenticate_credentials(payload)
        return (user,token)

    def leng_jwt(self,jwt_value):

        jwt_list=jwt_value.split()
        if len(jwt_list) !=3 or jwt_list[0].lower() !='ak7' or jwt_list[2].lower() !='auth':
            return None
        #返回token
        return jwt_list[1]


