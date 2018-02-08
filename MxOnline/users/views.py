from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, Banner
from django.db.models import Q
from .forms import LoginForm, RegisterForm
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from utils.send_email import send_register_email


# 登陆视图
class CustomBackend(ModelBackend):
    # 自定义authenticate方法满足需求
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))  # 取出user对象
            if user.check_password(password):  # 因为django存储的密码是密文，不能直接取出password
                # 所以才用check_password的方法内部检验
                return user
        except Exception as e:
            return None


#  注册视图
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name  # 这里的user_name是前端传过来的email
            user_profile.email = user_name
            # user_profile.set_password(pass_word)  # 保存密码
            user_profile.password = make_password(pass_word)  # 保存密码和上一行的操作意义一样
            user_profile.save()  # 这个就很尴尬了，非要加上force_inser=True才能从前端提交保存到数据库
            #但是我直接在后代文件中写save()就可以保存了，则会是为什么？？？
            # 然后几天之后我直接调用save方法居然又能行了，这是真的尴尬了
            send_register_email(user_name, 'register')
        return render(request, "index.html")



class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, "index.html")
        else:
            return render(request, "login.html", {'msg': '用户名或者密码错误！', 'login_form': form})


