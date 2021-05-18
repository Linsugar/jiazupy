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
from app.Serialiaers.UserSerializers import User_Serializers, Image_Serializers, feedback_Serializers, \
    release_Serializers, roog_Serializers, UserInfo_Serializers, wx_Serializers, SendTask_Serializers, \
    review_Serializers, teams_Serializers
from app.models import User, User_token, User_Image, Dynamic_Image, feedback, releasenew, weixinartic, sendtask, \
    Dynamic_review
from app.untils.Aut import Jwt_Authentication
from app.untils.UoOssFile.connectBucket import Bucket_Handle
from app.untils.rongyun.roog import rongyun
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
        rong = rongyun()
        oc = {
            "msg":None,
            "token": None,
            "avaror_iamge":None,
            "user_id":None,
            "user_name":None
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
            roogtoken = rong.register_roog(name=obj1.username, user_id=obj1.user_id, portraitUri=obj1.avator_image)['token']
            print('roottoken:'+roogtoken)
            User_token.objects.update_or_create(
                token_id=User.objects.filter(user_mobile=user_mobile).first(),
                defaults={
                    'user_token':roogtoken
                })
            oc['token'] = self.token
            oc['msg'] = "登录成功"
            oc['avator_image'] = obj1.avator_image
            oc['user_id'] = obj1.user_id
            oc['roogtoken'] = roogtoken
            oc['user_name'] = obj1.username

            return JsonResponse(oc)
        else:
            try:
                filpath = request.FILES.get("avator_image", None)
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
                roogtoken = rong.register_roog(name=request.data['username'],user_id=userid,portraitUri=upResult["url"])['token']
                User_token.objects.update_or_create(
                    token_id=User.objects.filter(user_mobile=user_mobile).first(),
                    user_token=roogtoken)
                Redata["token"] = serializer.token
                Redata["msg"] = "注册成功"
                Redata["roogtoken"] =roogtoken
                return JsonResponse(Redata)
            except Exception as e:
                oc['msg']='不存在'
                return JsonResponse(oc)
class UserInfo(GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = UserInfo_Serializers
    def list(self, request, *args, **kwargs):
        user_id=request.query_params.get("user_id")
        quer = User.objects.exclude(user_id=user_id).all()
        queryset = self.filter_queryset(quer)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
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
        user_name = request.data['up_name']
        up_avator = request.data['up_avator']
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
        updata={
            "user_id":user_id,
            "Old_Imagename":str(filpath),
            "New_Imagename":str(new_filename),
            "Up_ImageUrl":json.dumps(uplist),
            "Up_Title":up_title,
            "Up_Context":up_context,
            "Up_addres":up_addres,
            "Up_name":user_name,
            "Up_avator":up_avator,
        }
        serializer = self.get_serializer(data=updata)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(updata)
# 获取所有动态
class DynamicAll(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Image_Serializers
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        query = Dynamic_Image.objects.exclude(user_id=user_id).all()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pass

# 动态评论
class DynamicRevicew(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = review_Serializers
    def list(self, request, *args, **kwargs):
        query = Dynamic_review.objects.filter(review_rd=request.query_params.get("review_rd")).all()
        queryset = self.filter_queryset(query)
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

class Rongyun(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = roog_Serializers
    authentication_classes = [Jwt_Authentication]
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):

        rongid = request.data.get("token_id")
        rong = rongyun()
        result = {
            'msg': '获取成功',
            'coode': '200',
            'token': None
        }
        if User.objects.filter(user_id=rongid).exists():
            roogtoken = rong.register_roog(user_id=rongid,)['token']
            User_token.objects.update_or_create(
                token_id=User.objects.filter(user_id=rongid).first(),
                defaults={
                    'user_token':roogtoken
                })
            result['token']=roogtoken
            return JsonResponse(data=result,safe=False)
        else:
            result['coode'] = 400
            result['token'] = ''
            return JsonResponse(data=result, safe=False)

class Wxarticle(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = wx_Serializers
    def list(self, request, *args, **kwargs):
        query = weixinartic.objects.all()
        queryset = self.filter_queryset(queryset=query)
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

# 发布任务
class SendTaskView(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = SendTask_Serializers
    def list(self, request, *args, **kwargs):
        taskcls = request.query_params.get('taskcls')
        taststatue = request.query_params.get('taststatue')
        query = sendtask.objects.filter(taskcls=taskcls,taststatue=taststatue).all()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data,safe=False)
    def create(self, request, *args, **kwargs):
        task = random.randint(100000000,300000000)
        data = {
            'task':task,
            'tasksendid':request.data.get('tasksendid'),
            'tasksendname':request.data.get('tasksendname'),
            'taststatue':request.data.get('taststatue'),
            'taskcls':request.data.get('taskcls'),
            'taskcontent':request.data.get('taskcontent'),
            'tasktitle':request.data.get('tasktitle'),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED,safe=False)
# 领取任务记录
class TaskOnly(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = SendTask_Serializers
    def list(self, request, *args, **kwargs):
        taskid = request.query_params.get('taskid')
        taststatue = request.query_params.get('taststatue')
        if(taststatue == ''):
            query = sendtask.objects.filter(taskid=taskid).exclude(taststatue=1).all()
            queryset = self.filter_queryset(query)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            query = sendtask.objects.filter(taskid=taskid,taststatue=taststatue).all()
            queryset = self.filter_queryset(query)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse(serializer.data,safe=False)
    # 领取任务
    def create(self, request, *args, **kwargs):
        taskid = request.data.get("taskid")
        task = request.data.get("task")
        taststatue = request.data.get("taststatue")
        rs = sendtask.objects.filter(task=task).update(taststatue=taststatue, taskid=taskid)
        print(rs)
        result = {
            'msg':'更新成功',
            'statue':201
        }
        return JsonResponse(result,status=status.HTTP_201_CREATED,safe=False)


"""
团队管理,创建团队，查询团队
"""
class Team_Manger(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = teams_Serializers
    def create(self, request, *args, **kwargs):
        teamuid = random.randint(100000000000,900000000000)
        Team_Cover= []
        filelist = request.FILES.getlist("Team_Cover")
        for ifile in filelist:
            gettime = str(time.time())
            sptime = gettime.split('.')
            path = default_storage.save('untils/somename.jpg', ContentFile(ifile.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            upResult = Bucket_Handle().Upload_File(filename=sptime[0] + sptime[1] + ".jpg", filepath=tmp_file)
            Team_Cover.append(upResult["url"])
            print("===============================")
        data={
            'Team_uid':teamuid,
            'Team_name':request.data.get('Team_name'),
            'Team_init':request.data.get('Team_init'),
            'Team_Type':request.data.get('Team_Type'),
            'Team_Size':request.data.get('Team_Size'),
            'Team_Cover':json.dumps(Team_Cover),
            'Team_Introduction':request.data.get('Team_Introduction'),
            'Team_City':request.data.get('Team_City'),
            'Team_Score':request.data.get('Team_Score'),
            'Team_sex':request.data.get('Team_sex'),
            'Team_Dismissaltime':request.data.get('Team_Dismissaltime'),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)