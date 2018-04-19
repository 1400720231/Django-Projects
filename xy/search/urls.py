from django.conf.urls import url, include
from .views import All_Results

urlpatterns = [
    url(r'^all_results/$',All_Results,name='all_results'),
]