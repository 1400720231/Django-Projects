from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('username','birth','mobile')
	list_filter = ('username','birth','mobile',)
	search_fields = ['username','birth','mobile']

	class Meta:
		verbose_name='用户管理'
		verbose_name_plural = verbose_name

admin.site.register(UserProfile,UserProfileAdmin)