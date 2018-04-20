from django.conf.urls import url, include
from .views import All_Results,SearchList

urlpatterns = [
    url(r'^all_results/$',All_Results,name='all_results'),
    url(r'^search_list/$',SearchList,name='search_list'),
]