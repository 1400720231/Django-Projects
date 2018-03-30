from django.conf.urls import url
from . import views

urlpatterns = [
	# 博客标题视图函数
	url(r'^$', views.blog_title, name='blog_title'),

]