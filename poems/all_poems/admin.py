from django.contrib import admin
from .models import Poems, Author
# Register your models here.

class PoemsAdmin(admin.ModelAdmin):
	list_display = ('title','author','times','tag','collection','content')
	list_filter = ('title','author','times','tag','collection','content',)
	search_fields = ['title','tsg','collection','content','author','times']

	class Meta:
		verbose_name='诗词管理'
		verbose_name_plural = verbose_name

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_filter = ('name',)
	search_fields = ['name']

	class Meta:
		verbose_name='诗人管理'
		verbose_name_plural = verbose_name

admin.site.register(Author,AuthorAdmin)


admin.site.register(Poems,PoemsAdmin)