
from rest_framework.serializers import ModelSerializer,ValidationError,JSONField,CharField
import re

from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from app.models import User, User_Image, Dynamic_Image, feedback, releasenew, User_token, weixinartic, sendtask


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
    class Meta:
        model = Dynamic_Image
        fields = "__all__"

    def validate(self, attrs):
        print('发布动图：%s'%attrs)
        print("进入图片")
        return  attrs
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

# class review_Serializers(ModelSerializer):
#     class Meta:
#         model = Dynamic_review
#         fields = '__all__'
#     def validate(self, attrs):
#         print("进去review_Serializers")
#         return attrs