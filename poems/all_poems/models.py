from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name='作者',default='',null=True,blank=True)
    about_author = models.TextField(verbose_name='关于作者',default='',null=True,blank=True)
    class Meta:
        verbose_name='诗人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Poems(models.Model):
    author = models.ForeignKey(Author,verbose_name='诗人',default=1,null=True,blank=True)
    times = models.CharField(max_length=50, verbose_name='年代',default='',null=True,blank=True)
    title = models.CharField(max_length=50, verbose_name='诗词名',default='',null=True,blank=True)
    tag = models.CharField(max_length=50, verbose_name='标签',default='',null=True,blank=True)
    collection  = models.CharField(max_length=50, verbose_name='作品集',default='',null=True,blank=True)
    content = models.TextField(verbose_name='内容',default='',null=True,blank=True)
    explains = models.TextField(verbose_name='原文解释',default='',null=True,blank=True)
    view_nums = models.IntegerField(verbose_name='浏览次数',default=0)
    
    class Meta:
        verbose_name='诗词信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title