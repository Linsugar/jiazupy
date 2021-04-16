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
urlpatterns = [
    path('',include(rou.urls))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)