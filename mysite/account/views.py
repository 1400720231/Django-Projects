from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


from .forms import LoginForm


def user_login(request):
	if request.method == 'post':
		login_form = LoginForm(request.POST)
		if login_form.is_vaild():
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