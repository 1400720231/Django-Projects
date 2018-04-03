from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login # 这些是内置函数而不是视图函数，视图函数会自带模板，麻烦。。。
from django.contrib.auth import logout  # 这个是logout函数,参数是request
from users.models import UserProfile
from .forms import LoginForm, RegisterForm,UpDateInfoForm
from operations.models import UserLog
# 登录视图函数
def user_login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			user = authenticate(username=cd['username'],password=cd['password'])
			if user:
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
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
	return HttpResponseRedirect(reverse('index'))



# 注册视图
def RegisterView(request):
	if request.method == 'GET':
		register_form = RegisterForm()
		return render(request, 'register.html',{'form':register_form,'mes':''})
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get('username','')
			if UserProfile.objects.filter(username=user_name):
				return render(request, 'register.html',{'mes':'用户已经存在！'})
			else:
				pass_word = request.POST.get('password','')
				user_profile = UserProfile()
				user_profile.username = user_name
				user_profile.set_password(pass_word)
				user_profile.save()
				return HttpResponseRedirect(reverse('index'))
		else:
			return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/users/login/')
def User_Info(request):
	
	if request.method =='GET':
		old_info = UserProfile.objects.get(id=request.user.id)
		info = UpDateInfoForm(instance=old_info)
		context = {
		'info': info
		}
		return render(request,'user_info2.html', context=context)
	else:
		old_info = UserProfile.objects.get(id=request.user.id)
		info_form = UpDateInfoForm(data=request.POST,instance=old_info)
		if info_form.is_valid():
			info_form.save(commit=True)
		return HttpResponseRedirect(reverse('users:user_info'))
		

# 订单详情函数

def Order_List(request):
	if request.method == 'GET':
		user_logs = UserLog.objects.filter(user=request.user).order_by('-time')
		return render(request, 'order_list.html',{'user_logs':user_logs})


# 正在进行中的订单
def on_position(request):
	if request.method == 'GET':
		# 获取正在进行中的车位记录，按道理讲是室友一个在进行中的
		try:
			position = UserLog.objects.get(user=request.user,stop_pick='1')
		except UserLog.DoesNotExist:
			position = ''

		# 为空的时候赋值‘’ 不然前端会保存
	
		
	return render(request, 'on_position.html',{'position':position})
