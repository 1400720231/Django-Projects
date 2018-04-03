from django.db import models
from users.models import UserProfile
from positions.models import CarPosition
# Create your models here.
"""
用户操作日志表单

"""
class UserLog(models.Model):
	user = models.ForeignKey(UserProfile,verbose_name='用户')
	car_position = models.ForeignKey(CarPosition,verbose_name='车位')
	time = models.DateTimeField(auto_now_add=True,verbose_name='操作时间')
	stop_pick = models.CharField(max_length=5,choices=(('1','停车'),('0','取车')),default='1',verbose_name='停取车')
	pay_money = models.IntegerField(default=0,verbose_name='取车付款金额')
	class Meta:
		verbose_name='操作日志'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.user.username +'的操作记录'