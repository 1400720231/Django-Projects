from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserLog
from positions.models import CarPosition
from users.models import UserProfile
# Create your views here.
from django.contrib.auth.decorators import login_required
from utils.get_hours import get_hours


# 车位预定试图函数
@login_required(login_url = '/users/login/')
def order_position(request,position_id):
	if request.method == 'GET':
		user_status = request.user.status
		if user_status == '1':
			return HttpResponse('您已经在使用车位，不能再预定！')
		else:
			# 获取要预定的车位
			userlog_form = UserLog()
			position = CarPosition.objects.get(id=position_id)
			position.is_occupied = '1'
			position.save()
			# 预定车位成功
			userlog_form.user = request.user
			userlog_form.car_position = position
			userlog_form.stop_pick  = '1'
			userlog_form.save()
			# user 状态改为正在使用
			userprofile =UserProfile.objects.get(id=request.user.id)
			userprofile.status = '1'
			userprofile.save()
			return HttpResponse('您已经成功预定好'+position.position_name+'号车位')


# 取消车位预定视图函数
@login_required(login_url = '/users/login/')
def unorder_position(request, position_id):
	if request.method == 'GET':
		# 获取正在站位的position信息
		position = UserLog.objects.get(id = position_id)
		car_position = CarPosition.objects.get(id=position.car_position.id)
		time_this = position.time
		time_last = UserLog.objects.filter(user=request.user,stop_pick='0').order_by('-time')[0].time
		hours = get_hours(time_new=time_this, time_old=time_last)
		money = position.car_position.price*hours
		position.pay_money = money
		position.stop_pick = '0'
		position.save()
		car_position.is_occupied = '0'
		car_position.save()
		user = request.user
		user.status = '0'
		user.save()
		return HttpResponse('付款成功')
