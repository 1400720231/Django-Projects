from django.contrib import admin

# Register your models here.
from .models import BlogArticles


class BlogArtcilesAdmin(admin.ModelAdmin):
	list_display = ("title","author","publish")  #使用 list_display去控制哪些字段会显示在Admin的修改列表页面中。
	list_filter = ("publish","author") #置激活激活Admin	修改列表页面右侧栏中的过滤器,应该是一个列表或元组
	search_fields = ("title","body") # 设置启用Admin	更改列表页面上的搜索框。此属性应设置为每当有人在该文本框中提交搜索查询将搜索的字段名称的列表。
	# raw_id_fields = ("author",)\
	"""
默认情况下,Django	的Admin	对 ForeignKey字段使用选择框表示(<select>)。
有时候你不想在下拉菜单中显示所有相关实例产生的开销。
raw_id_fields是一个字段列表,你希望将ForeignKey	
或ManyToManyField转换成Input Widget
	"""
	date_hierarchy = "publish"
	ordering = ['publish','author']  # 排序，先让publish排序，再以author排序默认升序


admin.site.register(BlogArticles, BlogArtcilesAdmin)