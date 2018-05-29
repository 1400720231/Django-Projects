from django.contrib import admin
from .models import Poems
# Register your models here.

class PoemsAdmin(admin.ModelAdmin):
	list_display = ('title','author','times','poem_type','collection','content')
	list_filter = ('title','author','times','poem_type','collection','content',)
	search_fields = ['title','poem_type','collection','content','author','times']

	class Meta:
		verbose_name='诗词管理'
		verbose_name_plural = verbose_name

admin.site.register(Poems,PoemsAdmin)