from django.conf.urls import url,include
from .views import Comments,Praise_poems
urlpatterns = [

    url(r'^comments/(?P<poem_id>\d+)/$',Comments,name='comments'),
    url(r'^praise/(?P<poem_id>\d+)/$',Praise_poems,name='praise'),

 
]
