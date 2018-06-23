# 系统包
from datetime import datetime


#三方包
from django.db import models
from django.contrib.auth.models import AbstractUser



# 自定义的包



# 个人信息
class UserProfile(AbstractUser):
	"""
	用户数据表
	"""
	name = models.CharField(max_length=30,null=True,blank=True,verbose_name='姓名')
	birthday = models.DateField(null=True,blank=True,verbose_name='出生年月')
	gender = models.CharField(max_length=6,choices=(('mela','男'),('female','女')),verbose_name='性别')
	mobile = models.CharField(max_length=11,verbose_name='电话')
	email = models.EmailField(max_length=100,null=True,blank=True,verbose_name='邮箱')

	class Meta:
		verbose_name='用户'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.username


class VerifyCode(models.Model):
	"""
	短息验证码数据表

	notes:
		default=datatime.now 生成的时间是记录生成的时间，即数据库实例化的时间
		default=datatime.now() 生成的时间是代码编译的时间
	"""
	code =models.CharField(max_length=10, default ='',verbose_name='验证码')
	mobile = models.CharField(max_length=11,verbose_name='电话',default='')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name='短信验证码'
		verbose_name_plural= verbose_name

	def __str__(self):
		return self.code