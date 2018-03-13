# coding:utf-8
# author:mini_panda
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


# Course表单注册
class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    inlines = [LessonInline]

    # 当我们把is_banner=True的课程分开管理之后，这个Course应该是剩下的is_banner=False的
    # 所以我们添加筛选函数

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        return qs.filter(is_banner=False)

    # 重写self.save()方法， 实现额外功能
    def save_models(self):
        # 保存Course实例的时候把，ForeignKey的Organization中的字段course_nums + 1
        # 表示Organization下的某个实例又被多引用了一次， 即某个机构的课程数+ 1
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


"""
 准备把Course表单根据is_banner字段来分成两个表注册管理
 1> 在model中复制表Course：
     class BannerCourse(Course):
        class Meta:
            verbose_name = "轮播课程"
            verbose_name_plural = verbose_name
            proxy = True  # 很重要，一定是True，不然会在数据库生成新的表BannerCourse
 2> 在xadmin中向注册其他表单一样注册，但是记得
    定义queryset()函数筛选出必要管理的数据，即：is_banner = True
"""


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    inlines = [LessonInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        return qs.filter(is_banner=True)


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']  # course__name 表示链接到外键Course的name字段


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)