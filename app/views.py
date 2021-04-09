import random

from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet,generics
from rest_framework import mixins, status
from app.Serialiaers.UserSerializers import User_Serializers,Image_Serializers
from app.models import User, User_token, User_Image, Dynamic_Image
from app.untils.Md5Catch import Power
from app.untils.UoOssFile.connectBucket import Bucket_Handle


class JiaUser(GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = User_Serializers
    def list(self, request, *args, **kwargs):
        user_mobile = request.query_params['user_mobile']
        user_pwd = request.query_params['user_pwd']
        get_queryset = User.objects.filter(user_mobile=user_mobile,user_pwd=user_pwd).first()
        queryset = self.filter_queryset(queryset=get_queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=False)
        return JsonResponse(serializer.data,safe=False)

    def create(self, request, *args, **kwargs):
        userid = random.randint(1000000000,80000000000)
        Redata ={
            'user_id':userid,
            'invite_number':666666,
            'platform':request.data['platform'],
            'deviceid':request.data['deviceid'],
            'user_mobile':request.data['user_mobile'],
            'user_pwd':request.data['user_pwd'],
            'user_name':request.data['user_name'],
            'avator_image':'333',
            'city':request.data['city'],
            'create_ip':request.META.get("REMOTE_ADDR"),
        }
        Rp = {
            'msg':None,
            'token':None,
            'coode':None
        }
        mobile = request.data['user_mobile']
        obj = User.objects.filter(user_mobile=mobile).first()
        if not obj:
            # 进行加密
            serializer = self.get_serializer(data=Redata)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            User_Md5 = Power().Power_Md5(mobile)
            obj1 = User.objects.filter(user_mobile=request.data['user_mobile']).first()
            User_token.objects.update_or_create(token_id=obj1, defaults={'user_token': User_Md5})
            Rp['msg']="注册成功"
            Rp['token']=User_Md5
            Rp['coode']="2001"
            Rp['userid']=userid
        else:
            Rp['msg'] = "您输入的手机号已存在"
            Rp['coode'] = "2004"
        return Response(Rp)


class DynamicImage(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Image_Serializers
    def list(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        query = Dynamic_Image.objects.filter(user_id=user_id).all()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.FILES.get("image", None)
        filpath =  request.FILES.get("image", None)
        tempFilePath = filpath.temporary_file_path()
        new_filename = request.data['new_filename']
        up_title = request.data['up_title']
        up_context=request.data['up_context']
        up_addres= request.data['up_addres']
        user_id = request.data['user_id']
        upResult = Bucket_Handle().Upload_File(filename=new_filename,filepath=tempFilePath)
        updata={
            'user_id':user_id,
            'Old_Imagename':str(filpath),
            'New_Imagename':str(new_filename),
            'Up_ImageUrl':upResult['url'],
            'Up_Title':up_title,
            'Up_Context':up_context,
            'Up_addres':up_addres,
        }
        serializer = self.get_serializer(data=updata)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(updata)