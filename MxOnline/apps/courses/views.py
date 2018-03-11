from django.shortcuts import render, reverse
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mini_utils import LoginRequireMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')  # 按照时间添加的逆序排序，降序，即最新顺序

        hot_course = Course.objects.all().order_by('-click_num')[:3]

        # 全局搜索功能 关键词语： icontains 如同sql中的like语句 i表示不区分大小写
        search_keywords = request.GET.get('keywords', "")  # 取不到默认为空
        if search_keywords:    # Q函数相当于or 的意思 要么name以keywors开头，要么desc，要么detail以keywords开头
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(detail__icontains=search_keywords)|Q(desc__icontains=search_keywords))


        # 课程排序
        sort = request.GET.get('sort', "")  # 找不到就为空''
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_num')
        # 对course分页,这里是第三方库pagenation的内置格式，只是换了一下数据字段
        try:
            page = request.GET.get('page', 1)  # 这个page字段是安装库后自己有的，不用管
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        # 教程文档中没有3这个参数，其实个参数在源码中是per_page,这个参数表示每页显示几个的意思
        courses = p.page(page)
        context = {

            'all_courses': courses,
            'sort': sort,  # 把sort传回去，做html选择状态
            'hot_course': hot_course
        }
        return render(request, 'course-list.html', context)


class VideoPlayView(View):
    """
    视频播放页视图函数

    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course  # lesson是Video表中的字段，且外键指向Course表,course收Course中的字段
        # 查询是否已经关联该课程，就是看usercourse表里面有没有
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 为空则没有关联， 强行关联save()一下
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        all_resource = CourseResource.objects.filter(course=course)  # 用get的话只能获得一个资源文件，filter筛选所有满足的资源文件
        # 筛选出所有学过该课程的queryset对象
        user_courses = UserCourse.objects.filter(course=course)
        # 列表推导获取所有user_id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 所有课程 user_id__in(双下划线) 表示user_id  in 意思是只要user_id在后面的list里面就可以了
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        # 获取学过的相关课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:4]
        context = {
            'course': course,
            'all_resource': all_resource,
            'relate_courses': relate_courses,
            'video': video
        }
        return render(request, "course-play.html", context)


class CourseDetailView(View):
    """课程详情页"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1  # 点击数加1
        course.save()
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        context = {
            'course': course,
            'relate_courses': relate_courses
        }
        return render(request, 'course-detail.html', context)


class CourseInfoView(LoginRequireMixin, View):  # 装饰器在点击我要学习的时候会跳入登录页面
    """
    课程章节信息，通过点击我要学习 点击进来
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1  # 访问此链接，学习人数加1
        course.save()
        # 查询是否已经关联该课程，就是看usercourse表里面有没有
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 为空则没有关联， 强行关联save()一下
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        all_resource = CourseResource.objects.filter(course=course)  # 用get的话只能获得一个资源文件，filter筛选所有满足的资源文件
        # 筛选出所有学过该课程的queryset对象
        user_courses = UserCourse.objects.filter(course=course)
        # 列表推导获取所有user_id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 所有课程 user_id__in(双下划线) 表示user_id  in 意思是只要user_id在后面的list里面就可以了
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        # 获取学过的相关课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:4]
        context = {
            'course':course,
            'all_resource': all_resource,
            'relate_courses': relate_courses
        }
        return render(request, "course-video.html", context)


# 如果是函数写法的话就用@login_required,但是这里是类的写法所以继承我们写好的装饰器方法
class CommentsView(LoginRequireMixin, View):
    """评论功能页面"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)  # 用get的话只能获得一个资源文件，filter筛选所有满足的资源文件
        # 筛选出所有学过该课程的queryset对象
        user_courses = UserCourse.objects.filter(course=course)
        # 列表推导获取所有user_id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 所有课程 user_id__in(双下划线) 表示user_id  in 意思是只要user_id在后面的list里面就可以了
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        # 获取学过的相关课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:4]
        context = {
            'course': course,
            'all_resource': all_resource,
            'relate_courses': relate_courses
        }
        return render(request, "course-video.html", context)


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_anthenticated():
            # 判断用户状态
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status": "success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg":"添加失败"}', content_type='application/json')



