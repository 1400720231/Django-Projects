from django.contrib import admin

# Register your models here.
from .models import CarPosition



class CarPositionAdmin(admin.ModelAdmin):
	list_display = ('position_name','is_occupied','price')
	list_filter = ('position_name','is_occupied','price',)
	search_fields = ['position_name','is_occupied','price']

	class Meta:
		verbose_name='车位信息'
		verbose_name_plural = verbose_name

admin.site.register(CarPosition,CarPositionAdmin)