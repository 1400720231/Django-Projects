# 声明该app的配置文件
default_app_config = "courses.apps.CoursesConfig"

"""
apps.py:

class CoursesConfig(AppConfig):
    name = 'courses'
    verbose_name = "课程管理"  # 新增的地方，意思是该app别名为课程管理，在后台体现出来

"""