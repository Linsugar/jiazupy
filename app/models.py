from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class User(models.Model):
    # 用户唯一id
    user_id = models.CharField(max_length=21,unique=True)
    # 用户头像
    avator_image =models.CharField(max_length=100)
    # 创建时ip地址
    create_ip = models.CharField(max_length=21)
    # 用户名
    user_name = models.CharField(max_length=8)
    # 用户名密码
    user_pwd = models.CharField(max_length=15)
    # 城市
    city  = models.CharField(max_length=16)
    # 邀请码
    invite_number = models.IntegerField()
    # 生日
    birthday = models.DateTimeField(auto_now_add=True)
    # 用户手机
    user_mobile = models.CharField(max_length=13,unique=True)
    #注册时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 设备id
    deviceid = models.CharField(max_length=64)
    # 设备平台
    platform =models.CharField(max_length=15)
    # 最后登录时间
    last_login = models.DateTimeField(auto_now=True)

class User_token(models.Model):
    token_id = models.OneToOneField(to=User,on_delete=models.CASCADE,unique=True)
    user_token = models.CharField(max_length=240)

class User_Image(models.Model):
    user_id = models.OneToOneField(to=User,on_delete=models.CASCADE,unique=True)
    Up_Time = models.TimeField(auto_now=True)
    Up_ImageUrl = models.ImageField('照片',upload_to='%Y/%m/%d/')



