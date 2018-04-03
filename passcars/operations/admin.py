from django.contrib import admin

# Register your models here.
from .models import UserLog

class UserLogAdmin(admin.ModelAdmin):
	list_display = ('user','car_position','time','stop_pick','pay_money')
	list_filter = ('user','car_position','time','stop_pick','pay_money',)
	search_fields = ['user_username','car_position','time','stop_pick','pay_money']
	class Meta:
		verbose_name='车位预定记录'
		ordering = ['-time']

"""

user = models.ForeignKey(UserProfile,verbose_name='用户')
	car_position = models.ForeignKey(CarPosition,verbose_name='车位')
	time = models.DateTimeField(auto_now_add=True,verbose_name='操作时间')
	stop_pick
"""


admin.site.register(UserLog,UserLogAdmin)