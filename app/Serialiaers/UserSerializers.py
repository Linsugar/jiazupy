from rest_framework.serializers import ModelSerializer

from app.models import User, User_Image, Dynamic_Image


class User_Serializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        print("进入")
        return  attrs

class Image_Serializers(ModelSerializer):
    class Meta:
        model = Dynamic_Image
        fields = "__all__"

    def validate(self, attrs):
        print('发布动图：%s'%attrs)
        print("进入图片")
        return  attrs



