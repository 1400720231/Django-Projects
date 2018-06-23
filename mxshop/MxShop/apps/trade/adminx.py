import xadmin
from .models import ShoppingCart ,OrderInfo, OrderGoods






"""
# Course表单注册
class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
  
xadmin.site.register(BannerCourse, BannerCourseAdmin)
"""

class ShoppingCartAdmin(object):
    list_display = ['user', 'goods', 'nums', 'add_time']
    search_fields = ['user', 'goods', 'nums', 'add_time']
    list_filter = ['user', 'goods', 'nums', 'add_time']



class OrderInfoAdmin(object):
	list_display = ['user','order_sn','trade_no','pay_status','post_script','order_mount','pay_time',
					'address','signer_name','signer_mobile','add_time']
	search_fields = ['user','order_sn','trade_no','pay_status','post_script','order_mount','pay_time',
					'address','signer_name','signer_mobile','add_time']
	list_filter = ['user','order_sn','trade_no','pay_status','post_script','order_mount','pay_time',
					'address','signer_name','signer_mobile','add_time']




class OrderGoodsAdmin(object):
	list_display =['order','goods','goods_num','add_time']
	serach_fields =['order','goods','goods_num','add_time']
	list_fiter = ['order','goods','goods_num','add_time']




xadmin.site.register(ShoppingCart, ShoppingCartAdmin)

xadmin.site.register(OrderInfo, OrderInfoAdmin)

xadmin.site.register(OrderGoods, OrderGoodsAdmin)