from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = '博客管理'# 此行为新增内容，将app的中文名字(别名)设置成“博客管理”
