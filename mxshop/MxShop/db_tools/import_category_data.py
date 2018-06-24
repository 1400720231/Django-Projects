# -*- coding: utf-8 -*-
# 用脚本独立使用django的model，相关文档地址：  https://docs.djangoproject.com/en/1.11/topics/settings/
import sys
import os

# 获取当前文件的路径的目录，即：data/文件夹
# 这里不用os.path.insert的里理由是不像setting.py文件下BASE_DIR可以参考
# 获取当前文件的文件夹，即db_tools/
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 把db_tools的上级目录(MxShop)追加在python环境变量中
sys.path.append(pwd)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")
# 初始化呢django
import django
django.setup()
# ---------------------------------------------------------------------

from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_intance = GoodsCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()

"""
原来的路径代码为:
    pwd = oos.path.dirname(os.path.realpath(__file__))
    os.path.append(pwd+'../')
其中pwd表示含有setting.py文件的MxShop文件夹的路径,pwd+'../'表示整个项目文件夹MxShop文件夹路径,看是没有问题,
但是整个代码会报错：ImportError: No module named 'MxShop'，说MxShop不存在这个MODULE,即使按照百度把MxShop.setting改成
MxShop.Mxshop.setting也不行.


解决带方法一(在pycharm环境下能导入数据,但是不能单独python执行脚本):
    用pycharm手动把MxShop(不是含有setting.py的那个MxShop文件夹，是含有setting.py的那个
MxShop文件夹的上一级)标记为source_root才行．

解决方法二(在pycahrm环境下可以导入数据,也可以单独执行python脚本,肯定推荐使用这种):
    # 在原有的pwd外面再套一个os.path.dirname()函数,而不是用../的方式获取整个项目的文件夹路径.
    pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    os.path.append(pwd)
"""