from django.contrib.auth.models import AbstractUser

from django.db import models
class User(AbstractUser):
    # 用户唯一id
    user_id = models.CharField(max_length=21,unique=True)
    # 用户头像
    avator_image = models.TextField()
    # 创建时ip地址
    create_ip = models.CharField(max_length=21)
    # 城市
    city= models.CharField(max_length=16)
    # 邀请码
    invite_number = models.IntegerField()
    # 生日
    birthday = models.DateTimeField(auto_now_add=True)
    # 用户手机
    user_mobile = models.CharField(max_length=13,unique=True)
    #注册时间
    create_time = models.CharField(max_length=64)
    # 设备id
    deviceid = models.CharField(max_length=64)
    # 设备平台
    platform =models.CharField(max_length=15)
    # 最后登录时间
    last_login = models.DateTimeField(auto_now=True)
    #用户加入的团队
    user_team = models.CharField(max_length=64,null=True)
    #用户积分
    user_score = models.IntegerField(default=0)
    # 用户等级
    user_level = models.IntegerField(default=0)
    #用户性别
    user_sex = models.CharField(max_length=12)

class User_token(models.Model):
    token_id = models.OneToOneField(to=User,on_delete=models.CASCADE,unique=True)
    user_token = models.CharField(max_length=240)

class User_Image(models.Model):
    user_id = models.OneToOneField(to=User,on_delete=models.CASCADE,unique=True)
    Up_Time = models.TimeField(auto_now=True)
    Up_ImageUrl = models.ImageField('照片',upload_to='%Y/%m/%d/')

# 发布动态
class Dynamic_Image(models.Model):
    user_id = models.CharField(max_length=16)
    Up_Time = models.CharField(max_length=64)
    Old_Imagename = models.CharField(max_length=64)
    New_Imagename = models.CharField(max_length=64)
    Up_ImageUrl = models.TextField()
    Up_Context = models.CharField(max_length=200)
    Up_Title = models.CharField(max_length=64)
    Up_addres = models.CharField(max_length=16)
    Up_name = models.CharField(max_length=16)
    Up_avator= models.TextField()
    Dynamic_Id = models.CharField(max_length=64)

# 动态评论
class Dynamic_review(models.Model):
    review_userid = models.CharField(max_length=32)
    recview_avator = models.TextField()
    review_content = models.CharField(max_length=64)
    review_name = models.CharField(max_length=16)
    review_time = models.CharField(max_length=64)
    review_bool = models.IntegerField(default=0)
    review_dynamicid = models.CharField(max_length=64)

# 反馈
class feedback(models.Model):
    feed_id = models.CharField(max_length=20)
    feed_createID = models.CharField(max_length=64)
    feedback_context = models.TextField()
    feedback_time = models.CharField(max_length=64)
    # 反馈处理人
    feedback_dealpeople = models.CharField(max_length=20,default='Tang')
    feedback = models.CharField(max_length=64,default='等待处理')

class releasenew(models.Model):
    news_id = models.CharField(max_length=16)
    news_title = models.CharField(max_length=64)
    news_context = models.TextField()
    news_url = models.URLField()
    news_avatimage = models.URLField()
    news_username = models.CharField(max_length=16)
    user_id = models.CharField(max_length=32)
    news_time = models.CharField(max_length=64)


class sendtask(models.Model):
    ClsChoice = (
        (1, '初级任务'),
        (2, '中级任务'),
        (3, '高级任务'),
    )
    #任务Id
    task = models.CharField(max_length=16)
    # 任务分类
    taskcls = models.IntegerField(choices=ClsChoice,default=1)
    # 任务发布时间
    tasktime = models.CharField(max_length=64)
    # 任务标题
    tasktitle= models.CharField(max_length=16)
    # 任务内容
    taskcontent = models.TextField()
    # 领取状态
    taststatue = models.IntegerField(default=1)
    # 领取人id
    taskid = models.CharField(max_length=64,null=True)
    # 发布任务id
    tasksendid = models.CharField(max_length=64,default='23607016397')
    #发布任务人名称
    tasksendname = models.CharField(max_length=64,default='管理员')


"""
Team_uid:团队唯一id,Team_name:团队名字,Team_init:团队创始人,
Team_Type:团队类型,Team_Size:团队规模,Team_Rank:团队等级,
Team_Cover:团队封面,Team_Introduction:团队介绍,Team_City:团队可加入城市,
Team_Score:团队可加入积分,Team_sex:团队可加入性别,Team_time:团队创建时间,
Team_Dismissaltime：团队解散时间
"""
class Teams(models.Model):
    Team_uid = models.CharField(max_length=64,unique=True)#团队唯一id
    Team_name =models.CharField(max_length=16) #团队名字
    Team_init = models.CharField(max_length=32)#团队创始人
    Team_initid = models.CharField(max_length=64)#团队创始人id
    Team_Type = models.CharField(max_length=16)#团队类型
    Team_Size = models.IntegerField()#团队规模
    Team_Rank = models.IntegerField(default=1)#当前团队等级
    Team_Cover = models.TextField()#团队封面
    Team_Introduction = models.TextField(max_length=64,null=True)#团队介绍
    Team_City = models.CharField(max_length=10,null=True)#团队可加入城市
    Team_level = models.IntegerField(default=0)#团队可加入等级
    Team_Score = models.IntegerField(null=True)#团队可加入积分
    Team_sex = models.CharField(null=True,max_length=12)#团队可加入性别
    Team_time = models.CharField(max_length=64)
    Team_Dismissaltime = models.DateTimeField(null=True)#团队解散时间

class Videosmodel(models.Model):
    video_Title = models.CharField(max_length=16)
    video_Time = models.CharField(max_length=64)
    video_context = models.TextField()
    video_upusername = models.CharField(max_length=16)
    video_upuserid = models.CharField(max_length=64)
    video_url = models.TextField()
    video_cover = models.TextField()

# 招聘信息
class Recruitment(models.Model):
    # 招聘唯一id
    recruitment_createid = models.CharField(max_length=64,unique=True)
    # 招聘发起者id
    recruitment_id  = models.CharField(max_length=32)
    # 招聘类型
    recruitment_type = models.CharField(max_length=16)
    # 招聘岗位
    recruitment_job = models.CharField(max_length=24)
    # 招聘工资
    recruitment_money  = models.CharField(max_length=16)
    # 招聘地点
    recruitment_address = models.CharField(max_length=64,default="待定")
    # 招聘公司
    recruitment_company = models.CharField(max_length=64,default="待定")
    # 招聘发起者
    recruitment_person = models.CharField(max_length=64)
    # 招聘宣传图
    recruitment_Image = models.TextField(null=True)
    # 招聘宣传内容/大概介绍
    recruitment_Content = models.TextField()
    # 招聘方式
    recruitment_Phone = models.CharField(max_length=64)
    # 招聘创建时间
    recruitment_time = models.CharField(max_length=64)

# 视频列表
class VideosTabs(models.Model):
    video_id = models.CharField(max_length=64,unique=True)
    video_Time = models.CharField(max_length=64)
    video_Title = models.CharField(max_length=24)
    # 视频上传者
    video_User = models.CharField(max_length=64)
    # 视频封面
    video_Image = models.TextField(null=True)
    # 视频内容
    video_Content = models.CharField(max_length=264,null=True)
    video_url = models.TextField()

# 视频评论
class VideosReviews(models.Model):
    Review_id = models.CharField(max_length=64)
    Review_name = models.CharField(max_length=12)
    Review_User = models.CharField(max_length=64)
    Review_photo = models.CharField(max_length=164)
    Review_time = models.CharField(max_length=64)
    Review_Content = models.CharField(max_length=64)