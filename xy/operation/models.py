from django.db import models

# Create your models here.
class LogMessage(models.Model):
    history = models.CharField(max_length=100,verbose_name='历史搜索',default='')
    date = models.DateTimeField(auto_now_add=True)