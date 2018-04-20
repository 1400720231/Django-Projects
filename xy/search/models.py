from django.db import models

# Create your models here.
class JobboleArticle(models.Model):
    title = models.CharField(max_length=60, verbose_name='文章标题',default='',null=True,blank=True)  #标题
    create_date = models.CharField(max_length=30, verbose_name='发表时间',default='',null=True,blank=True)
    front_image_url = models.CharField(max_length=400, verbose_name='封面图地址',default='',null=True,blank=True)# 封面图链接地址
    url = models.CharField(max_length=400, verbose_name='文章链接',default='',null=True,blank=True)  # 链接
    url_object_id =models.CharField(max_length=30, verbose_name='url_id',default='',null=True,blank=True)  #url_id http://blog.jobbole.com/113817/ 113817则为其id
    praise_nums = models.CharField(max_length=100, verbose_name='点赞数',default='',null=True,blank=True)  # 点赞数
    comment_nums = models.CharField(max_length=100, verbose_name='评论数',default='',null=True,blank=True)  # 评论书
    fav_nums =models.CharField(max_length=100, verbose_name='收藏数',default='',null=True,blank=True)  # 收藏数
    tags = models.CharField(max_length=100, verbose_name='标签',default='',null=True,blank=True)# 标签
    content = models.TextField( verbose_name='文章内容',default='',null=True,blank=True) # 
    
    class Meta:
        verbose_name='伯乐在线文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


