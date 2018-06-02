from django.db import models
from user.models import UserProfile
from all_poems.models import Poems


# Create your models here.
# 评论
class Comments(models.Model):
	user = models.ForeignKey(UserProfile,verbose_name='评论用户')
	poem = models.ForeignKey(Poems,verbose_name='评论诗词')
	comments = models.TextField(verbose_name='评论内容')
	date_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

	class Meta:
		ordering = ['-date_time']
		verbose_name='评论信息'
		verbose_name_plural =verbose_name

	def __str__(self):
		return self.poem.title

# 点赞
class Praise(models.Model):
	user = models.ForeignKey(UserProfile,verbose_name='点赞用户')
	poem = models.ForeignKey(Poems,verbose_name='点赞诗词')


	class Meta:
		verbose_name='点赞信息'
		verbose_name_plural =verbose_name

	def __str__(self):
		return self.user.username