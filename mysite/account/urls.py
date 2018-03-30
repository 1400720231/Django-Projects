from django.conf.urls import url
from . import views
# from django.contrib.auth.views import logout  # 直接调用的logou视图函数内置模板文件的
urlpatterns = [
	url(r'^login/$',views.user_login, name='user_login'),
	url(r'^logout/$',views.user_logout, name='user_logout'),

]