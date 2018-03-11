from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, ModifyPwdForm2
from .forms import UserInfoForm
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from utils.send_email import send_register_email
from utils.mini_utils import LoginRequireMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from .models import Banner  # 轮播图


# 登陆视图 ModelBackend这个参数很重要！！！！！！！！记得回来复习
class CustomBackend(ModelBackend):
    # 自定义authenticate方法满足需求
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) |Q(email=username))  # 取出user对象
            if user.check_password(password):  # 因为django存储的密码是密文，不能直接取出password
                # 所以才用check_password的方法内部检验
                return user
        except Exception as e:
            return None


# 邮箱激活视图
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:  # 只要能筛选出来的都激活，因为有可能随机函数万一随机出来的字符串一样
            for record in all_records:
                email = record.email  # 获得email
                user = UserProfile.objects.get(email=email)  # 获得user信息
                user.is_active = True  # 是否激活改成True
                user.save()  # 保存到数据库
        return render(request, "login.html")


#  注册视图
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.get(email=user_name):  # 判断用户是否存在
                return render(request, "register.html", {'mes': '用户已存在'})
            else:
                pass_word = request.POST.get('password', '')
                user_profile = UserProfile()
                user_profile.username = user_name  # 这里的user_name是前端传过来的email
                user_profile.email = user_name
                user_profile.is_active = False  # 默认设置未激活
                # user_profile.set_password(pass_word)  # 保存密码
                user_profile.password = make_password(pass_word)  # 保存密码和上一行的操作意义一样
                user_profile.save()  # 这个就很尴尬了，非要加上force_inser=True才能从前端提交保存到数据库
                # 但是我直接在后代文件中写save()就可以保存了，则会是为什么？？？
                # 然后几天之后我直接调用save方法居然又能行了，这是真的尴尬了

                # 把注册信息写近 UserMessage表的， 在个人中心我的消息中体现
                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = "欢迎您的注册  ！！"
                user_message.save()
                send_register_email(user_name, 'register')
                return render(request, "login.html")
        else:
            return render(request, "login.html")


def LogoutView(request):
    logout(request)  # 登出
    # 登出后重定向到index页面
    return HttpResponseRedirect(
        reverse('index'))


# 登录视图
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
                if user.is_active:  # 是否激活，激活才让登录
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {'mes': '用户未激活'})
        else:
            return render(request, "login.html", {'msg': '用户名或者密码错误！', 'login_form': form})


class ForgetPwdViws(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", '')  # 获取前端穿过来的email值
            send_register_email(email, 'forget')   # 注册邮件发送完成，返回html
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 邮箱激活视图
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:  # 只要能筛选出来的都激活，因为有可能随机函数万一随机出来的字符串一样
            for record in all_records:
                email = record.email  # 获得email
                return render(request, 'password_reset.html', {'email': email})
        return render(request, "login.html")


class ModifyPwdView(View):
    """修改密码  """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            email = request.POST.get('email')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'mes': '密码不一致'})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'e mail': email, 'modify_form': modify_form})


class UserInfoView(LoginRequireMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html')

    """
    # 方法1 强行赋值save()
    def post(self, request):  # instance是一个已经存在的对象
        user_info_form = UserInfoForm(request.POST)
        if user_info_form.is_valid():
            address = user_info_form.cleaned_data['address']
            birth = user_info_form.cleaned_data['birth']
            mobile = user_info_form.cleaned_data['mobile']
            nick_name = user_info_form.cleaned_data['nick_name']
            request.user.address = address
            request.user.birth = birth
            request.user.mobile = mobile
            request.user.nick_name = nick_name
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')
    """
    # 方法2: 利用modelForm特性，instance=request.user save()
    def post(self, request):  # instance是一个已经存在的对象
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequireMixin, View):
    """
    用户头像修改
    上传文件用post方法
    知识点：admin或者xadmin用form字段为filefield的的时候可以都用户上传的头像做保存，利用这一点来修改头像文件
"""

    # 方法１：
    def post(self, request):
        # 文件类型，和input传入的值保存在不一样的地方，文件类型在request.FILES里面
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']  # clean_data是is_valid()通过后的键值对，以此来获取image
            request.user.image = image  # 给user.image赋值
            request.user.save()  # request.user保存,如果是instance的话就是image_form.save()

"""
    # 方法２（按道理这样是可以的，可是好像保存不到数据库。。。关键是我修改其他信息的时候也是用的instance方法是可以保存到数据库的，真是日了狗。。）
    def post(self, request):
        # 文件类型，和input类型传入的值保存在不一样的地方，input传入的值在request.POST里面，文件类型的传值在request.FILES里面
        #
        # form.ModelForm中独有的instance参数，意思是：例子,实质是一个你将要修改的实例的对象，这里是request.user对象，
        # save()后会直接替换掉原来user.image，因为UploadImageForm中的fields = ['image']
        
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
"""


class UpdatePwdView(View):
    """个人中心的更新用户密码， 此时已经登录了"""
    def get(self, request):
        modify_form = ModifyPwdForm2()
        context = {
            'form': modify_form
        }
        return render(request, 'user-info-modify_password.html', context)

    def post(self, request):
        modify_form = ModifyPwdForm2(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 != pwd2:
                return HttpResponse("密码不一致 ！！")
            else:
                user = request.user
                user.set_password(pwd2)
                user.save()
                return HttpResponseRedirect(reverse('login'))  # 修改成功后重定向到登录页面
        else:
            # 把表单的错误信息传回前端
            return HttpResponse(json.dumps(modify_form.errors))


class SendEmailCodeView(LoginRequireMixin, View):
    """
    发送邮箱验证码, 前提是登录条件下
    """
    def get(self, request):
        email = request.GET.get('email', '')  # 没有默认为空
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(View):
    """
    修改email
    用到了两个view，一个发送邮件，然后用ajax访问第二个view验证验证码的正确性来修改数据库
    用ajax的好处就是不用跳转页面，的确用户体验会好一点，

    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponseRedirect(reverse('users:update_email'))
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequireMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        context = {
            'user_courses': user_courses
        }
        return render(request, 'usercenter-mycourse.html', context=context)


class MyFavOrgView(LoginRequireMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id           # 获取收藏机构的id
            org = CourseOrg.objects.get(id=org_id)  # 获取某个机构对象
            org_list.append(org)  # 追加进去
        context = {
            'org_list': org_list
        }
        return render(request, 'usercenter-fav-org.html', context=context)


class MyFavTeacherView(LoginRequireMixin, View):
    """
    我收藏的授课教师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:  # 获取收藏教师的id
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)  # 获取单独的teacher对象
            teacher_list.append(teacher)   # 追加进去
        context = {
            'teacher_list': teacher_list
        }
        return render(request, 'usercenter-fav-teacher.html', context=context)


class MyFavCourseView(LoginRequireMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:  # 获取收藏教课程的id
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)  # 获取单独的course对象
            course_list.append(course)   # 追加进去
        context = {
            'course_list': course_list
        }
        return render(request, 'usercenter-fav-course.html', context=context)


class MymessageView(LoginRequireMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        # 把未读消息全部转换成已读
        for all_unread_message in all_unread_messages:
            all_unread_message.has_read = True
            all_unread_message.save()

        # 对机构分页,这里是第三方库pagenation的内置格式，只是换了一下数据字段
        try:
            page = request.GET.get('page', 1)  # 这个page字段是安装库后自己有的，不用管
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 3, request=request)  # 教程文档中没有3这个参数，其实个参数在源码中是per_page,这个参数表示每页显示几个的意思
        messages = p.page(page)

        context = {
            'messages': messages

        }
        return render(request, 'usercenter-message.html', context)


class IndexView(View):
    """
    index首页功能视图函数
    """
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')  # 排序一下
        courses = Course.objects.filter(is_banner=False)[:5]  # 非banner course
        banner_courses = Course.objects.filter(is_banner=True)[:3]  # banner  course
        course_orgs = CourseOrg.objects.all()[:15]  # 取15个
        context = {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs




        }
        return render(request, 'index.html', context)