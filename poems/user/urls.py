from django.conf.urls import url, include
from .views import Logout,User_Info,Register,Login,User_Praise
urlpatterns = [
	url(r'^logout/$', Logout, name='logout'),
	url(r'^info/$', User_Info, name='info'),
	url(r'^register/$', Register, name='register'),
	url(r'^login/$', Login, name='login'),
	url(r'^user_praise/$', User_Praise, name='user_praise'),

	
 ]
