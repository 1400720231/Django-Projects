from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login # 这些是内置函数而不是视图函数，视图函数会自带模板，麻烦。
from django.shortcuts import reverse
from django.contrib.auth import logout  # 这个是logout函数,参数是request
from .forms import RegisterForm,LoginForm,UpDateInfoForm
from .models import UserProfile
# 登出视图函数，直接调用内置登出函数logout
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('all_poems:all'))


def Info(request):
	return render(request,'user_info.html')

# 注册视图
def Register(request):
	if request.method == 'GET':
		register_form = RegisterForm()
		return render(request, 'register.html',{'form':register_form,'mes':''})
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get('username','')
			password = request.POST.get('password','')
			if UserProfile.objects.filter(username=user_name):
				return render(request, 'register.html',{'form':register_form,'mes':'用户已经存在！'})
			else:
				# 用户写入数据库　注册成功
				pass_word = request.POST.get('password','')
				user_profile = UserProfile()
				user_profile.username = user_name
				user_profile.set_password(pass_word)
				user_profile.save()
				# 马上登录
				user = authenticate(username=user_name,password=password)
				if user:
					login(request,user)
				return HttpResponseRedirect(reverse('all_poems:all'))
		else:
			return HttpResponseRedirect(reverse('all_poems:all'))


# 登录视图函数
def Login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			user = authenticate(username=cd['username'],password=cd['password'])
			if user:
				login(request,user)
				return HttpResponseRedirect(reverse('all_poems:all'))
			else:
				return render(request, 'login.html',{'form':login_form,'mes':'账号或密码错误！'})
		else:
			return render(request, 'login.html',{'form':login_form,'mes':'输入格式有误！'})
	else:
		login_form = LoginForm()
		context = {"form":login_form}
		return render(request, 'login.html',context=context)

# 个人信息视图函数
@login_required(login_url='/user/login/')
def User_Info(request):
	if request.method =='GET':
		old_info = UserProfile.objects.get(id=request.user.id)
		info = UpDateInfoForm(instance=old_info)
		context = {
		'info': info
		}
		return render(request,'user_info.html', context=context)
	else:
		old_info = UserProfile.objects.get(id=request.user.id)
		info_form = UpDateInfoForm(data=request.POST,instance=old_info)
		if info_form.is_valid():
			info_form.save(commit=True)
		return HttpResponseRedirect(reverse('user:info'))


def User_Praise(request):
	return render(request,'user_praise.html')