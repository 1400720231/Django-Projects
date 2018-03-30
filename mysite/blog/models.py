from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class BlogArticles(models.Model):
	title = models.CharField(max_length=30, verbose_name='标题',default='',null=True,blank=True)
	author = models.ForeignKey(User,related_name='blog_posts',verbose_name='作者')
	body = models.TextField(verbose_name='内容') # 大文本字段。该模型默认的表单组件是 	Textarea	 。
	publish = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		ordering = ("-publish",)
		verbose_name='博客文章'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.title
