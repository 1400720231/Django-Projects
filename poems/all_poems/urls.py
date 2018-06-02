from django.conf.urls import url,include
from django.views.generic import TemplateView 
from .views import All_Poems,Poem_Detail,All_Poets,Poet,Voice,SearchList,Get_Pinyin
urlpatterns = [
    # index页面的映射
    url(r'^index/$',TemplateView.as_view(template_name='index.html'),name='index'),
    # 所有诗集
    url(r'^all/$',All_Poems,name='all'),
    # 所有诗人
    url(r'^all_poets/$',All_Poets,name='all_poets'),
    # 某个诗人详情页
    url(r'^poet/(?P<poet_id>\d+)/$',Poet,name='poet'),
    #某首诗的详情页
    url(r'^poem_detail/(?P<poem_id>\d+)/$',Poem_Detail,name='poem_detail'),
    url(r'^voice/$',Voice,name='voice'),
    # 搜索视图函数
    url(r'^search/$',SearchList,name='search'),
    url(r'^pinyin/$',Get_Pinyin,name='pinyin'),

]

