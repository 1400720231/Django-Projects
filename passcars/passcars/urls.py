"""passcars URL Configuration

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
from django.contrib import admin
from django.views.generic import TemplateView 
from django.views.static import serve  # 处理meida文件静态文件的
from passcars.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',TemplateView.as_view(template_name='base.html'),name='index'),
    # users url
    url(r'^users/', include('users.urls', namespace='users')),
    # 车位app
    url(r'^positions/', include('positions.urls', namespace='positions')),
    # 用户操作
    url(r'^operations/', include('operations.urls', namespace='operations')),
     # 配置上传访问文件
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),


]
