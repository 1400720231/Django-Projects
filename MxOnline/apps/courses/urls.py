# coding:utf-8
# author:mini_panda
from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, VideoPlayView, CourseInfoView, CommentsView, AddCommentsView
urlpatterns =[
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程学习章节页面
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论功能
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comment'),
    url(r'^comment/$', AddCommentsView.as_view(), name='add_comments'),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

]


