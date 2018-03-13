"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from django.views.generic import TemplateView  # 专门处理静态文件的View
from django.views.static import serve  # 处理静态文件的

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdViws, ResetView, ModifyPwdView, LogoutView
from users.views import IndexView
from MxOnline.settings import MEDIA_ROOT
# STATIC_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^logout/$', LogoutView, name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),  # 邮箱激活的url
    url(r'^forget/$', ForgetPwdViws.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),  # 重置的get方法url
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),
    # 机构课程url配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace='course')),
    # 配置上传访问文件
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # debug=false 时配置static文件 访问地址
    # url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),
    # user.views
    url(r'^users/', include('users.urls', namespace='users'))
]


"""
1> handler404配置
    全局404 配置， 名字是固定写法，django会自动识别的：handler404
2> 处理404状态码的视图函数配置
    def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response
3> setting.py下记得把DEBUG=True 改为False
    不然输入不存在的访问地址的时候2>中的函数无效。返回不了2>中函数的'404.html页面'
4> ALLOWED_HOSTS = ['*']
     DEBUG = False的时候必须设置ALLOWED_HOSTS参数(原来为ALLOWED_HOSTS=[])， 
     这里的'*'表示所有客户端都可以访问
5> 静态文件重新访问服务配置
    当DEBUG=False的时候，你会发现所有没有了css样式，因为此时django不会再帮你默认管理
    这些样式文件了，一般来讲都是配置是再Apache，或者nginx上面的,所以我们像meida_root那样
    配置serve函数

"""
# 全局400 页面函数,
handler404 = 'users.views.page_not_found'
# 全局500 页面函数
handler500 = 'users.views.page_error'


