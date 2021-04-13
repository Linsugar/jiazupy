
from rest_framework.serializers import ModelSerializer,ValidationError,JSONField
import re
from app.models import User, User_Image, Dynamic_Image

class User_Serializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        print("进入")
        return  attrs
    # def validate_user_pwd(self,value):
    #     result = re.search('^[a-z][a-zA-Z0-9]{5,13}',str(value))
    #     if result:
    #        return value
    #     raise ValidationError(detail='请以英文字母开头,并且密码长度不低于6位')
    #


class Image_Serializers(ModelSerializer):
    class Meta:
        model = Dynamic_Image
        fields = "__all__"

    def validate(self, attrs):
        print('发布动图：%s'%attrs)
        print("进入图片")
        return  attrs


    # def validate_user_id(self,value):
    #     if User.objects.filter(user_id=value).exists():
    #         return value
    #     raise ValidationError(detail="您的信息有误")



