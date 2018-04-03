from django.conf.urls import url, include
from .views import order_position, unorder_position
urlpatterns = [
    url(r'^order/(?P<position_id>\d+)/$',order_position,name='order_position'),
    url(r'^unorder/(?P<position_id>\d+)/$',unorder_position,name='unorder_position'),
 

]
