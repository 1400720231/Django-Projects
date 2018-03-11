from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.db.models import Q
from .models import CourseOrg, CityDict, Teacher
# Create your views here.
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course


class OrgView(View):
    """课程机构列表功能 筛选功能等 所有机构页面"""
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 热门课程，按照click_nums倒序
        hot_orgs = all_orgs.order_by("-click_num")[0:3]
        # 城市
        all_citys = CityDict.objects.all()

        # 全局搜索功能 关键词语： icontains 如同sql中的like语句 i表示不区分大小写
        search_keywords = request.GET.get('keywords', "")  # 取不到默认为空
        if search_keywords:  # Q函数相当于or 的意思 要么name以keywors开头，要么desc 以keywords开头
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(
                    desc__icontains=search_keywords))

        # 下面的每次筛选就会重新复赋值给all_orgs，保证了all_orgs是满足筛选的
        # 筛选出城市
        city_id = request.GET.get('city', "")  # city的值来自于a标签：<a href="?city={{ city.id }}">
                                               # 传进来的是city.id是来自CotyDict queryset的实例创建id，数据库中的all_orgs的city_id是CityDict的外键，所以这种filter是对的
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))  # city字段是外键，在数据库中以city_id名字保存
            # CourseOrg中city字段是个CityDict对象(因为是外键)，但是在数据库中是以city_id字段保存，因为CourseOrg中的默认主键是id
        # 类别筛选
        category = request.GET.get('ct', "")
        # if True才会筛选 不然是无效的
        if category:
            all_orgs = all_orgs.filter(category=category)
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-course_nums")

        # 计数
        org_nums = all_orgs.count()

        # 对机构分页,这里是第三方库pagenation的内置格式，只是换了一下数据字段
        try:
            page = request.GET.get('page', 1)  # 这个page字段是安装库后自己有的，不用管
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)  # 教程文档中没有3这个参数，其实个参数在源码中是per_page,这个参数表示每页显示几个的意思
        orgs = p.page(page)
        context = {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,  # 回传city_id只是为了增加选中时候的判断功能
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        }
        return render(request, 'org-list.html', context)


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():  # 是否合法
            user_ask = userask_form.save(commit=True)  # commit属于ModelForm的方法
            # 如果是commit= False的话 user_ask就是一个model对象
            return HttpResponse("status: success")
        else:
            return HttpResponse("{'status': 'fail', 'msg':'添加出错'}")


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        # course_set表示反向取外键的值,也是queryset对象
        has_fav = False  # 判断是否收藏
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]  # 反向获取到teacher

        context = {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
                    }
        return render(request, 'org-detail-homepage.html', context)


class OrgCourseView(View):
    """
    课程首页
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # course_set表示反向取外键的值,也是queryset对象
        all_course = course_org.course_set.all()
        has_fav = False  # 判断是否收藏
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        """
        course teacher org是未了告诉前端页面刺客访问的是那教师，机构还是课程，为了收藏功能中的fav_type准备的
        并没有采用js实现，打算就用django后台逻辑实现
        """

        context = {
            'all_course': all_course,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav

        }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # course_set表示反向取外键的值,也是queryset对象
        # all_course = course_org.course_set.all()
        has_fav = False  # 判断是否收藏
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        context = {

            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav


        }
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    """
    教师介绍页
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # course_set表示反向取外键的值,也是queryset对象
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        context = {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav


        }
        return render(request, 'org-detail-teachers.html', context)


class AddFavView(View):
    """
        用户收藏，用户取消收藏, 这个功能是应ajax实现的
    """
    def post(self, request):

        # # has_fav = False
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 判断是否登录， return后面就不执行了，在这里结束了
        # 未登录状态下依然会有user类在里面
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        # 用户登录后逻辑
        exist_records = UserFavorite.objects.filter(user=request.user, fav_type=int(fav_type), fav_id=int(fav_id))
        if exist_records:
            # 记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:  #　如果不存在
            user_fav = UserFavorite()
            if int(fav_id) >0 and int(fav_type) >0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                has_fav = True  # 根据传回的值，判断是未收藏还是已收藏
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")

            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    """课程教师列表页面"""
    def get(self, request):
        all_teachers = Teacher.objects.all()
        sort = request.GET.get('sort', "")
        # 全局搜索功能 关键词语： icontains 如同sql中的like语句 i表示不区分大小写
        search_keywords = request.GET.get('keywords', "")  # 取不到默认为空
        if search_keywords:  # Q函数相当于or 的意思 要么name以keywors开头，要么desc 以keywords开头
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords)|
                Q(work_position__icontains=search_keywords))

        if sort:
            if sort == 'students':
                all_teachers = all_teachers.order_by("-click_num")
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]
        all_teacher_nums = all_teachers.count()

        try:
            page = request.GET.get('page', 1)  # 这个page字段是安装库后自己有的，不用管
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)  # 教程文档中没有3这个参数，其实个参数在源码中是per_page,这个参数表示每页显示几个的意思
        teachers = p.page(page)
        context = {
            'all_teachers': teachers,
            'sorted_teacher': sorted_teacher,
            'sort': sort,
            'all_teacher_nums': all_teacher_nums

        }
        return render(request, 'teachers-list.html', context)


class TeacherDetailView(View):
    """
    讲师的的详情页，和机构教师详情页是不一样的两个功能页面
    """
    def get(self, request, teacher_id):
        # 讲师
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        # 讲师的课程。通过course表filter出来
        all_courses = Course.objects.filter(teacher=teacher)
        # 热门讲师通过点击数来order_by
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]

        context = {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher
        }
        return render(request, 'teacher-detail.html', context)