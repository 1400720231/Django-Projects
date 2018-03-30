from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login # 这些是内置函数而不是视图函数，视图函数会自带模板，麻烦。。。
from django.contrib.auth import logout  # 这个是logout函数,参数是request


from .forms import LoginForm

# 登录视图函数
def user_login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			user = authenticate(username=cd['username'],password=cd['password'])
			if user:
				login(request,user)
				return HttpResponse('成功登陆用户！！')
			else:
				return HttpResponse("登陆失败，请检查您的帐号和密码！")
		else:
			return HttpResponse("输入内容格式不对，请重新输入！")
	else:
		login_form = LoginForm()
		context = {"form":login_form}
		return render(request, 'login.html',context=context)


# 登出视图函数，直接调用内置登出函数logout
def user_logout(request):
	logout(request)
	# 重定向到blog_title页面
	return HttpResponseRedirect(reverse('blog:blog_title'))
