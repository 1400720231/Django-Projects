# coding:utf-8
# author:mini_panda
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm


# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField()  # 验证码


# 忘记密码表单，用到了图片验证码库 caotcha，但是我总感觉这个库图片效果有点low
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()  # 验证


# 密码修改表单
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# 也是修改密码表单，只是我向试一下widget=forms.PasswordInput的功能，而已
class ModifyPwdForm2(forms.Form):
    password1 = forms.CharField(required=True, min_length=5, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, min_length=5, widget=forms.PasswordInput)


# 头像修改表单， 第二次用到ModelForm但是用到instance参数没有修改成功，这就很尴尬了
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # userprofile表
        fields = ['image']   # 修改的字段是image(头像)


# 修改其他信息的表单，用的也是Modelform, 而且我觉得修改已经存在的信息用ModelForm似乎更舒服一点
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birth', 'address', 'mobile']

