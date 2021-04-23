from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class User(AbstractUser):
    # 用户唯一id
    user_id = models.CharField(max_length=21,unique=True)
    # 用户头像
    avator_image =models.CharField(max_length=100)
    # 创建时ip地址
    create_ip = models.CharField(max_length=21)
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

class Dynamic_Image(models.Model):
    user_id = models.CharField(max_length=16)
    Up_Time = models.DateTimeField(auto_now=True)
    Old_Imagename = models.CharField(max_length=64)
    New_Imagename = models.CharField(max_length=64)
    Up_ImageUrl = models.TextField()
    Up_Context = models.CharField(max_length=200)
    Up_Title = models.CharField(max_length=64)
    Up_addres = models.CharField(max_length=16)
    Up_name = models.CharField(max_length=16)
    Up_avator= models.TextField()

class feedback(models.Model):
    feed_id = models.CharField(max_length=20)
    feedback_context = models.TextField()
    feedback_time = models.DateTimeField(auto_now=True)
    # 反馈处理人
    feedback_dealpeople = models.CharField(max_length=20,default='Tang')

class releasenew(models.Model):
    news_id = models.CharField(max_length=16)
    news_title = models.CharField(max_length=64)
    news_context = models.TextField()
    news_url = models.URLField()
    news_avatimage = models.URLField()
    news_username = models.CharField(max_length=16)
    user_id = models.CharField(max_length=32)
    news_time = models.DateTimeField(auto_now=True)


