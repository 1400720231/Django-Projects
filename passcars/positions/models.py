from django.db import models
"""
车位置的表单信息


"""
# Create your models here.
class CarPosition(models.Model):
	position_name = models.CharField(max_length=20,null=False,blank=False,verbose_name='车位名字')
	is_occupied = models.CharField(choices=(('1','正在使用'),('0','空位')),max_length=5,verbose_name='是否被占用',default='0')
	price = models.IntegerField(default=2,verbose_name='价格/小时')
	class Meta:
		verbose_name='车位信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.position_name