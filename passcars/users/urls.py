from django.conf.urls import url, include
from . import views

urlpatterns = [
	# login
    url(r'^login/$',views.user_login,name='login' ),
    # logout
    url(r'^logout/$', views.user_logout, name='logout'),
    # register
    url(r'^register/$', views.RegisterView, name='register'),
    # 个人中心
    url(r'^user_info/$', views.User_Info, name='user_info'),
    # 我的订详情页单
    url(r'^order_list/$', views.Order_List, name='order_list'),
    # 正在进行中的订单
    url(r'^on_position/$', views.on_position, name='on_position'),

]
  