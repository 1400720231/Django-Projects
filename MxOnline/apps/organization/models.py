from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市名称")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    category = models.CharField(max_length=20, verbose_name='机构类别',default='pxjg', choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')))
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo")
    # org/%Y/%m   Y当前时间的年份 m当前时间的月
    # image类型指明上传的途径，没有创建文件夹的话第一次上传的时候会自动创建的
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey(CityDict, verbose_name="所在城市")
    add_time = models.DateTimeField(auto_now_add=True)
    students =  models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        # 获取课程机构教师数量
        return self.teacher_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名称")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    point = models.CharField(max_length=50, verbose_name="教学特点")
    click_num = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(auto_now_add=True)
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", null=True, blank=True)
    age = models.IntegerField(default=18, verbose_name="年龄")
    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()

"""
    因为course中有一个外键指向了Teacher  teacher = models.ForeignKey(Teacher)
     course_set.all()表示获取所有指向此实例的course的 Query_set对象 
类似于course.objects.all()       
        
"""
