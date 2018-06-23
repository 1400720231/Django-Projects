from django.apps import AppConfig


class GoodsConfig(AppConfig):
    name = 'goods'
    #　修改xadmin后台别名
    verbose_name='商品'

"""
__init__.py下面：
default_app_config = "goods.apps.GoodsConfig"

apps.py:
class GoodsConfig(AppConfig):
    name = 'goods'
    verbose_name = "商品"  # 新增的地方，意思是该app别名为课程管理，在后台体现出来
"""