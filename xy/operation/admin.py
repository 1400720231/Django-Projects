from django.contrib import admin
from .models import LogMessage
# Register your models here.


class LogMessageAdmin(admin.ModelAdmin):
	list_display = ("history","date",'times')  #使用 list_display去控制哪些字段会显示在Admin的修改列表页面中。
	list_filter = ("history","date",'times') #置激活激活Admin	修改列表页面右侧栏中的过滤器,应该是一个列表或元组
	search_fields = ("history",) # 设置启用Admin	更改列表页面上的搜索框。此属性应设置为每当有人在该文本框中提交搜索查询将搜索的字段名称的列表。


admin.site.register(LogMessage, LogMessageAdmin)
