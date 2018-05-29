from django.conf.urls import url,include
from django.views.generic import TemplateView 
from .views import All_Poems,Poem_Detail
urlpatterns = [
    # index页面的映射
    url(r'^index/$',TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^all/$',All_Poems,name='all'),
    url(r'^poem_detail/(?P<poem_id>\d+)/$',Poem_Detail,name='Poem_Detail'),
]

