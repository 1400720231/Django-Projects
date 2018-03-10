# coding:utf-8
# author:mini_panda
from django.conf.urls import url, include
from .views import UserInfoView, MyCourseView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView
urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    # 头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    # 用户个人中心修密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # 验证并修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 我收藏的授课教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
]