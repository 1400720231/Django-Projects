from django.conf.urls import url, include
from . import views

urlpatterns = [

	# 所有的车位信息
    url(r'^all_positions/$',views.all_positions,name='all_positions' ),
    

]
