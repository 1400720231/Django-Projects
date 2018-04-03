# coding:utf-8
from datetime import datetime
import math
def get_hours(time_old,time_new):
	str1 = str(time_old)
	str2 = str(time_new)
	one = datetime.strptime(str1,'%Y-%m-%d %H:%M:%S.%f')
	two = datetime.strptime(str2,'%Y-%m-%d %H:%M:%S.%f')
	answer = two -one
	seconds = answer.seconds  # int
	hours = math.ceil(seconds/60/60)  # 转化小时
	return hours