
from rest_framework.serializers import ModelSerializer,ValidationError,JSONField,CharField
import re
from app.untils.Md5Catch import GetLocalTime
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from app.models import User, User_Image, Dynamic_Image, feedback, releasenew, User_token, sendtask, \
    Dynamic_review, Teams, Videosmodel, Recruitment, VideosTabs, VideosReviews


class User_Serializers(ModelSerializer):
    create_time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = User
        fields = "__all__"
    def validate(self, attrs):
        print("进入")
        user_mobile=attrs.get('user_mobile',None)
        password=attrs.get('password',None)
        check_user=User.objects.filter(user_mobile=user_mobile)
        user_obj=check_user.first()
        if user_obj is not None:
            if(User.objects.filter(user_mobile=user_mobile,password=password).exists()):
                payload = jwt_payload_handler(user_obj)
                self.token = jwt_encode_handler(payload)
                print(self.token)
                return attrs
            else:
                raise ValidationError(detail='密码不正确')
        else:
            self.create(attrs)
            check_user = User.objects.filter(user_mobile=user_mobile)
            user_obj = check_user.first()
            payload = jwt_payload_handler(user_obj)
            self.token = jwt_encode_handler(payload)
            return attrs
class UserInfo_Serializers(ModelSerializer):
    create_time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = User
        fields = "__all__"
    def validate(self,attrs):
        return attrs
class Image_Serializers(ModelSerializer):
    Up_Title = CharField(required=False, max_length=32, allow_blank=True,default="标题")
    Up_Context = CharField(required=False, max_length=300, allow_blank=True,default="标题")
    Up_Time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = Dynamic_Image
        fields = "__all__"

    def validate(self, attrs):
        Up_Title = attrs.get('Up_Title')
        Up_Context = attrs.get('Up_Context')
        if Up_Title.isnumeric():
            raise ValidationError(detail="您的标题不合法")
        elif Up_Title.isspace():
            raise ValidationError(detail="您的标题不合法")
        elif len(Up_Title) == 0:
            raise ValidationError(detail="标题不能为空")
        elif Up_Context.isnumeric() :
            raise ValidationError(detail="您的内容不合法")
        elif Up_Context.isspace():
            raise ValidationError(detail="您的内容不合法")
        elif len(Up_Context)==0:
            raise ValidationError(detail="内容过短")
        elif len(Up_Context)>200:
            raise ValidationError(detail="内容过长 ")
        return attrs
class feedback_Serializers(ModelSerializer):
    feedback_time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = feedback
        fields = "__all__"
    def validate(self, attrs):
        print('反馈：%s'%attrs)
        return attrs
# class roog_Serializers(ModelSerializer):
#     feedback_time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
#     class Meta:
#         model = feedback
#         fields = "__all__"
#
class release_Serializers(ModelSerializer):
    class Meta:
        model = User_token
        fields = "__all__"
    def validate(self, attrs):
        return attrs

class SendTask_Serializers(ModelSerializer):
    tasktime = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = sendtask
        fields = '__all__'

class review_Serializers(ModelSerializer):
    review_time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = Dynamic_review
        fields = '__all__'
    def validate(self, attrs):
        print("进去review_Serializers")
        return attrs

class teams_Serializers(ModelSerializer):
    Team_time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = Teams
        fields = '__all__'
    def validate(self, attrs):
        print("进去teams_Serializers")
        return attrs

class video_Serializers(ModelSerializer):
    video_Time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = Videosmodel
        fields = '__all__'
    def validate(self, attrs):
        print("进去video_Serializers")
        return attrs

class Recruitment_Serializers(ModelSerializer):
    recruitment_company = CharField(required=False, max_length=32, allow_blank=True,default="等待")
    recruitment_address = CharField(required=False, max_length=32, allow_blank=True,default="等待")
    recruitment_Phone = CharField(required=False, max_length=32, allow_blank=True,default="等待")
    recruitment_money = CharField(required=False, max_length=32, allow_blank=True,default="等待")
    recruitment_time = CharField(required=False, max_length=64, allow_blank=True,default=GetLocalTime().GetTimeYearTime())

    class Meta:
        model = Recruitment
        fields = '__all__'

    def validate(self, attrs):
        print("Recruitment_Serializers")
        if attrs.get('recruitment_type') == "招聘":
            if attrs.get('recruitment_company') == '':
                raise ValidationError(detail="公司不能为空")
            elif attrs.get('recruitment_address') == '':
                raise ValidationError(detail="公司地址不能为空")
            elif attrs.get('recruitment_money') == '':
                raise ValidationError(detail="请填写大概薪资范畴")
            elif attrs.get('recruitment_Content') == '':
                raise ValidationError(detail="请大概介绍一下吧")
            elif attrs.get('recruitment_Phone') == '':
                raise ValidationError(detail="请留下联系方式")
            else:
                return attrs
        else:
            if attrs.get('recruitment_Content') == '':
                raise ValidationError(detail="请大概介绍一下吧")
            elif attrs.get('recruitment_Phone') == '':
                raise ValidationError(detail="请留下联系方式")
            elif attrs.get('recruitment_money') == '':
                raise ValidationError(detail="请填写大概薪资范畴")
            else:
                return attrs

class Videos_Serializers(ModelSerializer):
    video_Time = CharField(required=False,max_length=64,allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    video_Title = CharField(required=False,allow_blank=True,max_length=64)
    video_User = CharField(required=False,allow_blank=True,max_length=64)
    video_Content = CharField(required=False,allow_blank=True,max_length=264)
    class Meta:
        model = VideosTabs
        fields = '__all__'

    def validate(self, attrs):
        print(attrs)
        image = attrs.get('video_Image')
        title = attrs.get('video_Title')
        content = attrs.get('video_Content')
        if len(image) <= 0:
            raise ValidationError(detail="请上传至少一张封面")
        elif len(title) <= 0 | len(title) >= 20:
            raise ValidationError(detail="标题不合法")
        elif title.isnumeric() | title.isdigit() | title.isspace() | len(title) >=20 | len(title) <=0:
            raise ValidationError(detail="标题不合法")
        elif content.isnumeric() | content.isdigit() | content.isspace() | len(content) >=200 | len(content) <=0:
            raise ValidationError(detail="标题不合法")
        return attrs


class VideoReviews_Serializers(ModelSerializer):
    Review_time = CharField(required=False,max_length=64,allow_blank=True,default=GetLocalTime().GetTimeYearTime())
    class Meta:
        model = VideosReviews
        fields = '__all__'
    def validate(self, attrs):
        result = attrs.get('Review_Content')
        if result.isnumeric() | result.isdigit() | result.isspace():
            raise ValidationError(detail="您输入的内容不合法")
        return attrs
