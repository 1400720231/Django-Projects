from django.contrib import admin

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('username','birth','mobile')
	list_filter = ('username','birth','mobile',)
	search_fields = ['username','birth','mobile']

	class Meta:
		verbose_name='用户信息表'
		verbose_name_plural = verbose_name

admin.site.register(UserProfile,UserProfileAdmin)