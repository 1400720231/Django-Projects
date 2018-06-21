# 系统包
from datetime import datetime

# 三方包
from django.db import models



from goods.models import Goods
from users.models import UserProfile
# Create your models here.
"""
# from django.contrib.auth import get_user_model
User = get_user_model()
get_auth_model()函数的作用是或者setting.py下面的AUTH_USER_MODEL
指定的数据库表，这样写就像xadmin改进的地方一样，在不知道用户数据表名字(UserProfile)的情况下，
直接获取setting.py下面的AUTH_USER_MODEL就可以了．


ps: 用这种方式会报错　尝试去解决　大师没有解决成功
报错代码：
	raise AppRegistryNotReady("Models aren't loaded yet.")

"""

class ShoppingCart(models.Model):
	"""
	购物车
	"""
	user = models.ForeignKey(UserProfile, verbose_name='用户')
	goods = models.ForeignKey(Goods, verbose_name='商品')
	nums = models.IntegerField(default=0, verbose_name='购买数量')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加书剑')


	class Meta:
		verbose_name='购物车'
		verbose_name_plural = verbose_name

	def __str__(self):
		return "%s(%d)".format(self.goods.name, self.goods_num)


class OrderInfo(models.Model):
	"""
    订单
	"""
	ORDER_STATUS = (
		("success","成功"), 
		("cancel","取消"), 
		("cancel","待支付"), 
	)
	user = models.ForeignKey(UserProfile,  verbose_name='用户')
	order_sn =models.CharField(max_length=30, unique=True, verbose_name='订单号')
	# 支付宝返回的订单号
	trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付宝订单号')
	pay_status = models.CharField(choices=ORDER_STATUS, max_length=10, verbose_name='订单状态')
	post_script = models.CharField(max_length=200, verbose_name='订单留言')
	order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
	pay_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
	# 用户信息
	address = models.CharField(max_length=100,  default="", verbose_name='收货地址')
	signer_name = models.CharField(max_length=20, default="",  verbose_name='签收人')
	signer_mobile = models.CharField(max_length=11, verbose_name='联系人电话')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name='订单'
		verbose_name_plural =verbose_name

	def __str__(self):
		return self.order_sn


class OrderGoods(models.Model):
	"""
	 订单的商品详情
	"""
	order = models.ForeignKey(OrderInfo, verbose_name='订单信息')
	goods = models.ForeignKey(Goods, verbose_name='商品')
	goods_num = models.IntegerField(default=0, verbose_name='商品数量')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name='订单商品'
		verbose_name_plural =verbose_name

	def __str__(self):
		return str(self.order.order_sn)