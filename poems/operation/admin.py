from django.contrib import admin
from .models import Comments,Praise
# Register your models here.

class CommentsAdmin(admin.ModelAdmin):
	list_display = ('user','poem','comments','date_time')
	list_filter = ('user','poem','comments','date_time',)
	search_fields = ['user','poem','comments','date_time']

	class Meta:
		verbose_name='评论管理'
		verbose_name_plural = verbose_name



class PraiseAdmin(admin.ModelAdmin):
	list_display = ('user','poem')
	list_filter = ('user','poem',)
	search_fields = ['user','poem']

	class Meta:
		verbose_name='点赞管理'
		verbose_name_plural = verbose_name

admin.site.register(Praise,PraiseAdmin)
admin.site.register(Comments,CommentsAdmin)