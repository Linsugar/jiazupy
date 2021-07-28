
from rest_framework.serializers import ModelSerializer,ValidationError,JSONField,CharField
import re

from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from app.models import User, User_Image, Dynamic_Image, feedback, releasenew, User_token, weixinartic, sendtask, \
    Dynamic_review, Teams, Videosmodel, Recruitment


class User_Serializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    print('111')

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
    class Meta:
        model = User
        fields = "__all__"
    print('111')
    def validate(self, attrs):
        print("1")
        return  attrs
class Image_Serializers(ModelSerializer):
    Up_Title = CharField(required=False, max_length=32, allow_blank=True,default="标题")
    Up_Context = CharField(required=False, max_length=300, allow_blank=True,default="标题")
    class Meta:
        model = Dynamic_Image
        fields = "__all__"

    def validate(self, attrs):
        print('发布动图：%s'%attrs)
        Up_Title = attrs.get('Up_Title')
        Up_Context = attrs.get('Up_Context')
        print(Up_Context)
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
    class Meta:
        model = feedback
        fields = "__all__"

    def validate(self, attrs):
        print('反馈：%s'%attrs)
        print("反馈")
        return attrs
class roog_Serializers(ModelSerializer):
    class Meta:
        model = feedback
        fields = "__all__"
class release_Serializers(ModelSerializer):
    class Meta:
        model = User_token
        fields = "__all__"

    def validate(self, attrs):
        print("进入release")
        return attrs

class wx_Serializers(ModelSerializer):
    class Meta:
        model=weixinartic
        fields = '__all__'

    def validate(self, attrs):
        print("进去wx_Serializers")
        return attrs

class SendTask_Serializers(ModelSerializer):
    class Meta:
        model = sendtask
        fields = '__all__'
    def validate(self, attrs):
        print("进去SendTask_Serializers")
        return attrs

class review_Serializers(ModelSerializer):
    class Meta:
        model = Dynamic_review
        fields = '__all__'
    def validate(self, attrs):
        print("进去review_Serializers")
        return attrs

class teams_Serializers(ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'
    def validate(self, attrs):
        print("进去teams_Serializers")
        return attrs

class video_Serializers(ModelSerializer):
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
