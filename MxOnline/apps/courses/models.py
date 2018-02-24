from django.db import models

# Create your models here.
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构',null=True, blank=True)  # 因为已经有数据存在，所以允许为空
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0,verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    category = models.CharField(verbose_name="课程类别",  max_length=20, default='后端开发')
    tag = models.CharField(verbose_name="课程标签",  max_length=20, default='')
    you_need_know = models.CharField(max_length=200, default='', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=200, default='', verbose_name='老师告诉你什么')

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_course_lesson(self):
        # 获取课程章节，是以地址链接的形式保存的并不是视频文件
        return self.lesson_set.all()

    def get_zj_nums(self):
        # 获取章节课程数
        # 因为lesson外键指向了Course，所以用lesson_set反向获取所有的lesson(章节数)
        return self.lesson_set.all().count()

    def get_learn_users(self):
        # 获取学习了该课程的用户
        return self.usercourse_set.all()[:5] # 取5个


    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        # 获取章节视频文件
        return self.video_set.all()


class Video(models.Model):

    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    add_time = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=200, verbose_name="访问地址", default='')
    # 也可以用models.URLField，但是就传入的数据必须是url格式
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name ="视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download  = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件")
    add_time= models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name