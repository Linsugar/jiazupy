import random
import time
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework.response import Response
import json
import os
from rest_framework.viewsets import GenericViewSet,generics
from rest_framework import mixins, status
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler
from app.Serialiaers.UserSerializers import User_Serializers, Image_Serializers, feedback_Serializers,release_Serializers
from app.models import User, User_token, User_Image, Dynamic_Image,feedback,releasenew
from app.untils.Aut import Jwt_Authentication
from app.untils.UoOssFile.connectBucket import Bucket_Handle
from jiazu import settings


class JiaUser(GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = User_Serializers
    def list(self, request, *args, **kwargs):
        user_id = request.query_params['user_id']
        get_queryset = User.objects.filter(user_id=user_id).first()
        queryset = self.filter_queryset(queryset=get_queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=False)
        return JsonResponse(serializer.data,safe=False)

    def create(self, request, *args, **kwargs):
        oc = {
            "msg":None,
            "token": None,
            "avaror_iamge":None,
            "user_id":None
        }
        userid = random.randint(1000000000,80000000000)
        user_mobile = request.data.get('user_mobile',None)
        password = request.data.get('password',None)
        obj = User.objects.filter(user_mobile=user_mobile).first()
        if obj:
            obj1 = User.objects.filter(user_mobile=user_mobile).get()
            if obj1.password !=password:
                return JsonResponse(data={"msg":"密码或手机号有误"})
            payload = jwt_payload_handler(obj)
            self.token = jwt_encode_handler(payload)
            oc['token'] = self.token
            oc['msg'] = "登录成功"
            oc['avator_image'] = obj1.avator_image
            oc['user_id'] = obj1.user_id
            return JsonResponse(oc)
        else:
            try:
                filpath = request.FILES.get("avator_image", None)
                print(filpath)
                gettime = str(time.time())
                sptime = gettime.split('.')
                path = default_storage.save('untils/somename.jpg', ContentFile(filpath.read()))
                tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                upResult = Bucket_Handle().Upload_File(filename=sptime[0] + sptime[1] + ".jpg", filepath=tmp_file)
                Redata = {
                    'user_id': userid,
                    'invite_number': 666666,
                    'platform': request.data['platform'],
                    'deviceid': request.data['deviceid'],
                    'user_mobile': user_mobile,
                    'password': request.data['password'],
                    'username': request.data['username'],
                    'avator_image': upResult["url"],
                    'city': request.data['city'],
                    'create_ip': request.META.get("REMOTE_ADDR"),
                }
                serializer = self.get_serializer(data=Redata)
                serializer.is_valid(raise_exception=True)
                Redata["token"] = serializer.token
                Redata["msg"] = "注册成功"
                return JsonResponse(Redata)
            except Exception as e:
                oc['msg']='不存在'
                return JsonResponse(oc)





class DynamicImage(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Image_Serializers
    authentication_classes = [Jwt_Authentication]
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id',None)
        if user_id is not None:
            query = Dynamic_Image.objects.filter(user_id=user_id).all()
            queryset = self.filter_queryset(query)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            query = Dynamic_Image.objects.filter(user_id=307844349484234).all()
            queryset = self.filter_queryset(query)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)



    def create(self, request, *args, **kwargs):
        uplist = []

        new_filename = request.data['new_filename']
        up_title = request.data['up_title']
        up_context = request.data['up_context']
        up_addres = request.data['up_addres']
        user_id = request.data['user_id']
        filpath =request.FILES.get("image", None)
        print(filpath)
        filelist = request.FILES.getlist("image")
        for ifile in filelist:
            gettime = str(time.time())
            sptime = gettime.split('.')
            path = default_storage.save('untils/somename.jpg', ContentFile(ifile.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            upResult = Bucket_Handle().Upload_File(filename=sptime[0]+sptime[1]+".jpg", filepath=tmp_file)
            uplist.append(upResult["url"])
            print("===============================")
            print(uplist)

        updata={
            "user_id":user_id,
            "Old_Imagename":str(filpath),
            "New_Imagename":str(new_filename),
            "Up_ImageUrl":json.dumps(uplist),
            "Up_Title":up_title,
            "Up_Context":up_context,
            "Up_addres":up_addres,
        }
        serializer = self.get_serializer(data=updata)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(updata)

class FeeBackView(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = feedback_Serializers
    authentication_classes = [Jwt_Authentication]
    def list(self, request, *args, **kwargs):
        feed_id = request.query_params.get('feed_id',None)
        obj = feedback.objects.filter(feed_id=feed_id).all()
        queryset = self.filter_queryset(obj)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data,safe=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RelMessage(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = release_Serializers

    def list(self, request, *args, **kwargs):
        obj = releasenew.objects.all()
        queryset = self.filter_queryset(obj)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        news_id = request.data.get("news_id")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)