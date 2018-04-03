from django import forms
from .models import UserProfile

# 登录表单
class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)  # <input type='password'>
	

# 注册表单
class RegisterForm(forms.Form):
	username = forms.CharField(max_length=20,required=True)
	password = forms.CharField(required=True, min_length=5,widget=forms.PasswordInput)


# 修改个人信息表单
class UpDateInfoForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['nick_name','birth','gender','address','mobile','username']
   