from django.db import models

# Create your models here.
class LogMessage(models.Model):
    history = models.CharField(max_length=100,verbose_name='历史搜索',default='')
    date = models.DateTimeField(auto_now_add=True,verbose_name="搜索时间")
    times = models.IntegerField(default=0,  null=True, blank=True,verbose_name="查询次数")
    class Meta:
        ordering = ('-date',)
        verbose_name='历史查询'
        verbose_name_plural = verbose_name