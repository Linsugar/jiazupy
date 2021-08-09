import random
import time
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models.query_utils import Q
from django.http import JsonResponse, QueryDict
from rest_framework.response import Response
import json
import os
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler
from app.Serialiaers.UserSerializers import User_Serializers, Image_Serializers, \
    release_Serializers, UserInfo_Serializers, SendTask_Serializers, \
    review_Serializers, teams_Serializers, video_Serializers, feedback_Serializers, Recruitment_Serializers, \
    Videos_Serializers, VideoReviews_Serializers
from app.models import User, User_token, Dynamic_Image, feedback, releasenew, sendtask, \
    Dynamic_review, Teams, Videosmodel, Recruitment, VideosTabs, VideosReviews
from app.untils.Aut import Jwt_Authentication
from app.untils.ossqiniu.connectBucket import Bucket_Handle
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
            "user_id":None,
            "user_name":None
        }
        userid = random.randint(1000000000,80000000000)
        user_mobile = request.data.get('user_mobile',None)
        password = request.data.get('password',None)
        obj = User.objects.filter(user_mobile=user_mobile).first()
        if obj:
            obj1 = User.objects.filter(user_mobile=user_mobile).get()
            print(obj1.password)
            if obj1.password != password:
                return JsonResponse(data={"msg":"密码或手机号有误"})
            payload = jwt_payload_handler(obj)
            self.token = jwt_encode_handler(payload)
            roogtoken = rong.register_roog(name=obj1.username, user_id=obj1.user_id, portraitUri=obj1.avator_image)['token']
            User_token.objects.update_or_create(
                token_id=User.objects.filter(user_mobile=user_mobile).first(),
                defaults={
                    'user_token':roogtoken
                })
            oc['token'] = self.token
            oc['msg'] = "成功"
            oc['avator_image'] = obj1.avator_image
            oc['user_id'] = obj1.user_id
            oc['roogtoken'] = roogtoken
            oc['user_name'] = obj1.username
            return JsonResponse(oc)
        else:
            try:
                result = request.data.copy()
                result.update({
                    'user_id': userid,
                    'create_ip': request.META.get("REMOTE_ADDR"),
                })
                serializer = self.get_serializer(data=result)
                res = serializer.is_valid(raise_exception=False)
                print(res)
                if res:
                    print(serializer.errors)
                    roogtoken = rong.register_roog(name=request.data['username'],user_id=userid,portraitUri=result["avator_image"])['token']
                    User_token.objects.update_or_create(
                        token_id=User.objects.filter(user_mobile=user_mobile).first(),
                        user_token=roogtoken)
                    Redata = {}
                    Redata["token"] = serializer.token
                    Redata["msg"] = "成功"
                    Redata["roogtoken"] = roogtoken
                    Redata["avator_image"] = result["avator_image"]
                    Redata["user_id"] = result["user_id"]
                    Redata["user_name"] = result["username"]
                    print(oc)
                    return Response(Redata)
                else:
                    oc['msg'] = '不存在'
                    return JsonResponse(oc)
            except Exception as e:
                print(e)
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


# 注册用户
class RegisterUser(GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    pass

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
            query = Dynamic_Image.objects.all().order_by('-id')
            queryset = self.filter_queryset(query)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            print(serializer.data)
            return JsonResponse(serializer.data,safe=False)
    def create(self, request, *args, **kwargs):
        msg = {
            "msg": "成功",
            "statues": status.HTTP_201_CREATED
        }
        new_filename = request.data['new_filename']
        image = request.data.get('image')
        Up_image = eval(str(image))
        result = request.data.copy()
        result.update({
            "Up_ImageUrl":json.dumps(Up_image),
            "New_Imagename": str(new_filename),
            "Old_Imagename": str('old'),
            "Dynamic_Id":random.randint(100000,90000000)
        })
        serializer = self.get_serializer(data=result)
        res = serializer.is_valid(raise_exception=False)
        if res is False:
            err = serializer.errors
            print(err)
            detail = err['non_field_errors'][0]
            msg.update({'msg': detail, 'statues': status.HTTP_400_BAD_REQUEST})
            return Response(msg)
        self.perform_create(serializer)
        return Response(msg)
# 获取所有动态
class DynamicAll(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    authentication_classes = [Jwt_Authentication]
    serializer_class = Image_Serializers
    def list(self, request, *args, **kwargs):
        query = Dynamic_Image.objects.order_by('-id')
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
    authentication_classes = [Jwt_Authentication]
    serializer_class = review_Serializers
    def list(self, request, *args, **kwargs):
        review_dynamic = request.query_params.get("review_dynamic")
        query = Dynamic_review.objects.filter(review_dynamicid=review_dynamic).all()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data,safe=False)

    def create(self, request, *args, **kwargs):
        result = {
            "msg": "成功",
            "code": 200
        }
        serializer = self.get_serializer(data=request.data)
        res = serializer.is_valid(raise_exception=False)
        print(serializer.errors)
        if res:
            result.update({
                "code":status.HTTP_200_OK
            })
            self.perform_create(serializer)
            return Response(result)
        else:
            result.update({
                "msg":"有误",
                "code":status.HTTP_400_BAD_REQUEST
            })
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FeeBackView(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = feedback_Serializers
    authentication_classes = [Jwt_Authentication]
    def list(self, request, *args, **kwargs):
        feed_id = request.query_params.get('feed_id',None)
        if feed_id is not None:
            obj = feedback.objects.filter(feed_id=feed_id).all()
            queryset = self.filter_queryset(obj)
            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse(serializer.data,safe=False)
        else:
            obj = feedback.objects.all()
            queryset = self.filter_queryset(obj)
            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)

    def create(self, request, *args, **kwargs):
        res = request.data.copy()
        res.update({
            "feed_createID":random.randint(100000000,300000000)
        })
        serializer = self.get_serializer(data=res)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
           "msg":"反馈成功",
            "code":200
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class FeedBackDeal(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    # 过滤反馈--回复反馈
    serializer_class = feedback_Serializers
    authentication_classes = [Jwt_Authentication]
    def list(self, request, *args, **kwargs):
        content = request.query_params.get("content")
        query = feedback.objects.filter(Q(feed_createID__contains=content)|Q(feedback__contains=content) |Q(feedback_context__contains=content))
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        fid = request.data.get('feed_id')
        feed_content = request.data.get("feed_content")
        fe = feedback.objects.get(feed_createID=fid)
        fe.feedback = feed_content
        fe.save()
        result = {
            "msg":"处理成功"
        }
        return Response(result)

class RelMessage(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = release_Serializers
    authentication_classes = [Jwt_Authentication]
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
    serializer_class = feedback_Serializers
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
    authentication_classes = [Jwt_Authentication]
    def list(self, request, *args, **kwargs):
        count = request.query_params.get("count")
        if count is None:
            count = 10
        appid = 'wx50f04c5bde8f1938'
        secret = '784069c669fd121a564a836dae2f1d8b'
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, secret)
        result = requests.get(url)
        rs = json.loads(result.content)
        print(rs)
        headers = {'Content-Type': 'application/json'}
        tokenurl = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=' + rs['access_token']
        data = {
            "type": "news",
            "offset": 0,
            "count": count
        }
        tilte = requests.post(url=tokenurl, data=json.dumps(data), headers=headers)
        con = tilte.content.decode('utf-8')
        return JsonResponse(con,safe=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# 发布任务
class SendTaskView(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = SendTask_Serializers
    authentication_classes = [Jwt_Authentication]
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
    authentication_classes = [Jwt_Authentication]
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
    authentication_classes = [Jwt_Authentication]
    queryset = Teams.objects.all()
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
        #     团队管理请求
        data={
            'Team_uid':teamuid,
            'Team_name':request.data.get('Team_name'),
            'Team_init':request.data.get('Team_init'),
            'Team_initid':request.data.get('Team_initid'),
            'Team_Type':request.data.get('Team_Type'),
            'Team_Size':request.data.get('Team_Size'),
            'Team_Cover':json.dumps(Team_Cover),
            'Team_Introduction':request.data.get('Team_Introduction'),
            'Team_City':request.data.get('Team_City'),
            'Team_Score':request.data.get('Team_Score'),
            'Team_level':request.data.get('Team_level'),
            'Team_sex':request.data.get('Team_sex'),
            'Team_Dismissaltime':request.data.get('Team_Dismissaltime'),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(serializer.data,safe=False)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class Videos(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = video_Serializers
    queryset = Videosmodel.objects.all()
    # authentication_classes = [Jwt_Authentication]
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# 返回七牛云token
import requests
import json
class GetQiNiuToken(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    def create(self, request, *args, **kwargs):
        QiuToken = Bucket_Handle().upToken()
        return Response(QiuToken)

    def list(self, request, *args, **kwargs):
        appid ='wx50f04c5bde8f1938'
        secret = '784069c669fd121a564a836dae2f1d8b'
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(appid,secret)
        result = requests.get(url)
        rs = json.loads(result.content)
        print(rs['access_token'])
        headers = {'Content-Type': 'application/json'}
        tokenurl = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token='+rs['access_token']
        data = {
            "type": "news",
            "offset": 0,
            "count": 2
        }
        tilte = requests.post(url=tokenurl,data=json.dumps(data),headers=headers)
        con = tilte.content.decode('utf-8')
        return Response(con)


class RecruitmentView(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    authentication_classes = [Jwt_Authentication]
    serializer_class = Recruitment_Serializers
    queryset = Recruitment.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        result = {
            "msg":"成功",
            "statues":200
        }
        Recruid = random.randint(100000000000,800000000000)
        mydict = request.data.copy()
        mydict.update({"recruitment_createid":Recruid})
        if request.data.get('recruitment_Image') is not None:
            Up_image = eval(str(request.data.get('recruitment_Image')))
            mydict.update({'recruitment_Image':json.dumps(Up_image)})
        serializer = self.get_serializer(data=mydict)
        res = serializer.is_valid(raise_exception=False)
        if res is False:
            err = serializer.errors
            print(err)
            detail = err['non_field_errors'][0]
            result.update({'msg':detail,'statues':status.HTTP_400_BAD_REQUEST})
            return Response(result)
        self.perform_create(serializer)
        result.update({'msg':"成功", 'statues': status.HTTP_201_CREATED})
        return Response(result)


class FilterRecruitment(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
    authentication_classes = [Jwt_Authentication]
    serializer_class = Recruitment_Serializers
    def list(self, request, *args, **kwargs):
        company =request.query_params.get('recruitment_company')
        money = request.query_params.get('recruitment_money')
        job = request.query_params.get('recruitment_job')
        print(money,company,job)
        query = Recruitment.objects.filter(Q(recruitment_company__contains=company) & Q(recruitment_money__contains= money) & Q(recruitment_job__contains=job))
        print(query)
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FilterDynamicImage(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    authentication_classes = [Jwt_Authentication]
    serializer_class = Image_Serializers

    def list(self, request, *args, **kwargs):
        filter_context = request.query_params.get('filter_context')
        query = Dynamic_Image.objects.filter(Q(Up_Context__contains=filter_context) | Q(Up_Title__contains=filter_context))
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class VideosList(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = Videos_Serializers
    # authentication_classes = [Jwt_Authentication]
    def create(self, request, *args, **kwargs):
        video_id = random.randint(100000000000,800000000000)
        mydict = request.data.copy()
        mydict.update({
            "video_id":video_id
        })
        serializer = self.get_serializer(data=mydict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        query = VideosTabs.objects.all()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class VideoFilter(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    authentication_classes = [Jwt_Authentication]
    serializer_class = VideoReviews_Serializers
    # 获取对应视频的评论
    def list(self, request, *args, **kwargs):
        Review_id = request.query_params.get('Review_id')
        query = VideosReviews.objects.filter(Review_id=Review_id).all()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 进行评论
    def create(self, request, *args, **kwargs):
        res = {
            "msg":"评论成功",
            "code":status.HTTP_200_OK
        }
        serializer = self.get_serializer(data=request.data)
        result = serializer.is_valid(raise_exception=False)
        if result:
            self.perform_create(serializer)
            return Response(res)
        else:
            err = serializer.errors
            print(err)
            detail = err['non_field_errors'][0]
            res.update({
                "msg": detail,
                "code":status.HTTP_400_BAD_REQUEST
            })
            return Response(res)