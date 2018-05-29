from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth import logout  # 这个是logout函数,参数是request

# 登出视图函数，直接调用内置登出函数logout
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('all_poems:all'))


