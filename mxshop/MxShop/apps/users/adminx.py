import xadmin
from .models import  UserProfile, VerifyCode



# class UserProfileAdmin(object):
# 	list_display = ['name','birthday','gender','mobile','email']
# 	search_fields = ['name','birthday','gender','mobile','email']
# 	list_filter = ['name','birthday','gender','mobile','email']



class VerifyCodeAdmin(object):
	list_display = ['code','mobile','add_time']
	search_fields =['code','mobile','add_time']
	list_filter = ['code','mobile','add_time']



# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(VerifyCode,VerifyCodeAdmin)