from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include
from app import views

rou = routers.DefaultRouter()
rou.register(viewset=views.JiaUser,prefix='user',basename="用户")
rou.register(viewset=views.DynamicImage,prefix='DyImage',basename="发布动态")
rou.register(viewset=views.FeeBackView,prefix='feedback',basename="反馈")
rou.register(viewset=views.RelMessage,prefix='Release',basename="实时新闻记录")
rou.register(viewset=views.Rongyun,prefix='rooyun',basename="获取token")
rou.register(viewset=views.UserInfo,prefix='userinfo',basename="获取当前用户")
rou.register(viewset=views.DynamicAll,prefix='dynamicall',basename="获取所有动态")
rou.register(viewset=views.Wxarticle,prefix='wxarticle',basename="获取所有的微信文章")
rou.register(viewset=views.SendTaskView,prefix='sendtask',basename="发布任务")
rou.register(viewset=views.TaskOnly,prefix='taskonly',basename="任务记录")
rou.register(viewset=views.DynamicRevicew,prefix='review',basename="动态评论")
rou.register(viewset=views.Team_Manger,prefix='team',basename="团队管理")
rou.register(viewset=views.Videos,prefix='video',basename="视频管理")
rou.register(viewset=views.GetQiNiuToken,prefix='qiniu',basename="视频管理")
rou.register(viewset=views.RecruitmentView,prefix='rec',basename="招聘管理")
rou.register(viewset=views.FilterRecruitment,prefix='fec',basename="招聘过滤")
rou.register(viewset=views.FilterDynamicImage,prefix='fdy',basename="动态过滤")
urlpatterns = [
    path('',include(rou.urls))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)