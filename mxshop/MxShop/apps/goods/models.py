from  datetime import datetime

from django.db import models
# 三方插件　富文本编辑器
from DjangoUeditor.models import UEditorField

# Create your models here.


class GoodsCategory(models.Model):
	"""
	商品类别
	DateTimeField DateField TiemFIeld 讲解地址：http://www.nanerbang.com/article/5488/
	help_text：
	related_name: 
	models.ForeignKey('self',[]): 表示外键指向自己，是为了实现自定义的产品父类类别(parents_type)从属关系，
		比如用此表建了一个实例对象叫＂肉类＂，又建立一个实例对象"食物类"，此时＂肉类＂的parents_type就可以指向
		来自同一个表的实例对象＂食物类＂．（其中parents_type允许为空）
	"""
	CATEGORY_TYPE = (
		(1,'一级类目'),
		(2,'二级类目'),
		(3,'三级类目'),
		)
	name = models.CharField(default='',max_length=30,verbose_name='类别名',help_text='类别名')
	code = models.CharField(default='',max_length=30,verbose_name='类别code',help_text='类别code')
	desc = models.TextField(default='',verbose_name='类别描述',help_text='类别描述 ')
	# 类级别
	category_type = models.IntegerField(choices=CATEGORY_TYPE,verbose_name='类目级别',help_text='类目级别')
	parents_type = models.ForeignKey('self',null=True,blank=True,verbose_name='父类目级',related_name='sub_cat')
	is_tab = models.BooleanField(default=False,verbose_name='是否导航',help_text='是否导航')
	add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

	class Meta:
		verbose_name='商品类目'
		verbose_name_plural =verbose_name

	def __str__(self):
		return self.name



class GoodsCategoryBrand(models.Model):
	"""
	品牌名字

	default=datetime.now表示实例创建的时间，即数据存保存的时候
	default=datetime.now()表示代码编译执行的时候时间
	"""
	category = models.ForeignKey(GoodsCategory,null=True,blank=True,verbose_name='商品类目')
	name = models.CharField(default='',max_length=30,verbose_name='品牌名',help_text='品牌名')
	desc = models.TextField(default='',max_length=200,verbose_name='品牌描述',help_text='品牌描述')	
	image = models.ImageField(upload_to="brands/  ")
	add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

	class Meta:
		verbose_name='品牌'
		verbose_name_plural =verbose_name

	def __str__(self):
		return self.name


class Goods(models.Model):
	"""
	商品
	UEditorField：
	"""
	category = models.ForeignKey(GoodsCategory,verbose_name='商品类目')
	goods_sn = models.CharField(max_length=50,default='',verbose_name='商品唯一货号')
	name = models.CharField(max_length=300,verbose_name='商品名')
	click_num = models.IntegerField(default=0,verbose_name='点击数')
	sold_num = models.IntegerField(default=0,verbose_name='商品销售量')
	fav_num = models.IntegerField(default=0,verbose_name='收藏数')
	goods_num = models.IntegerField(default=0,verbose_name='库存数')
	market_price = models.FloatField(default=0,verbose_name='市场价格')
	shop_price = models.FloatField(default=0,verbose_name='本店价格')
	goods_brief = models.TextField(max_length=500,verbose_name='商品简短描述')
	goods_desc = UEditorField(verbose_name='内容',imagePath='goods/images/',width=1000,height=300,
		filePath='goods/files/',default='')
	ship_free = models.BooleanField(default=True,verbose_name='是否承担运费')
	# 所有商品展示的封面图
	goods_front_image = models.ImageField(upload_to='goods/images/',null=True,blank=True,verbose_name='封面图')
	is_new = models.BooleanField(default=False,verbose_name='是否新品')
	is_hot = models.BooleanField(default=False,verbose_name='是否热销')
	add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

	class Meta:
		verbose_name='商品'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name



class GoodsImages(models.Model):
	"""
	商品轮播图（详情页的小图片轮播）
	"""
	goods = models.ForeignKey(Goods,verbose_name='商品',related_name='images')
	image = models.ImageField(upload_to="",verbose_name='图片',null=True,blank=True)
	image_url = models.CharField(max_length=300,null=True,blank=True,verbose_name='图片url')
	add_time =models.DateTimeField(default=datetime.now,verbose_name='添加时间')

	class Meta:
		verbose_name='商品轮播图'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.goods.name


class Banner(models.Model):
	"""
	轮播的商品（主页面的宽图轮播）
	"""
	goods = models.ForeignKey(Goods,verbose_name='商品')
	image = models.ImageField(upload_to='banner/',verbose_name='轮播图片')
	index = models.IntegerField(default=0,verbose_name='轮播顺序')
	add_time =models.DateTimeField(default=datetime.now,verbose_name='添加时间')

	class Meta:
		verbose_name='轮播商品'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.goods.name
