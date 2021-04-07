from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet,generics
from rest_framework import mixins, status
# Create your views here.
from app.Serialiaers.UserSerializers import User_Serializers,Image_Serializers
from app.models import User, User_token,User_Image
from app.untils.UoOssFile.connectBucket import Bucket_Handle


class JiaUser(GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = User_Serializers
    queryset = User.objects.all()
    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(queryset=self.queryset)
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data,safe=False)

    def create(self, request, *args, **kwargs):
        Rp = {
            'msg':None,
            'token':None,
            'coode':None
        }
        from app.untils.Md5Catch import Power
        user_mobile = request.data['user_mobile']
        User_Md5 = Power().Power_Md5(user_mobile)
        obj = User.objects.filter(user_mobile=user_mobile).first()
        if not obj:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            Rp['msg']="注册成功"
            Rp['token']=User_Md5
            Rp['coode']="2001"
            return Response(Rp)
        else:
            User_token.objects.update_or_create(user=obj,defaults={'user_token': User_Md5})
            Rp['msg'] = "登录成功"
            Rp['token'] = User_Md5
            Rp['coode'] = "2002"
            return Response(Rp)
        # return Response(status=status.HTTP_201_CREATED)


class ImageCheck(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    queryset = User_Image.objects.all()
    serializer_class = Image_Serializers
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print(request.FILES.get("image", None))
        print(request.data)
        finame = "imag"
        filpath =  request.FILES.get("image", None)
        Rp = {
            'msg': None,
            'token': None,
            'coode': None
        }
        obj = User.objects.filter(user_id=2).first()
        if not obj:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            Rp['msg'] = "注册成功"
            Rp['coode'] = "2001"
            return Response(Rp)
        elif not request.FILES['image']:
            return Response("没有文件")
        else:
            User_Image.objects.update_or_create(user_id=obj, defaults={'Up_ImageUrl': filpath})
            Rp['msg'] = "登录成功"
            Rp['coode'] = "2002"
            return Response(Rp)