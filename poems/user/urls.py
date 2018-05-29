from django.conf.urls import url, include
from .views import Logout
urlpatterns = [
	url(r'^logout/$', Logout, name='logout'),
 ]
