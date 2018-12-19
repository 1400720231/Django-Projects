from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')


'''
    #这里的index.html文件只是一个承载信息的前端文件，浏览器访问127.0.0.1:8000就显示一个在index.
    html页面上的信息，而不是访问127.0.0.1：8000/index.html,所以说这里的index.html
    与访问url地址是无关的，取决于learning_logs/urls.py中的url(r'') 的正则表示是匹配
'''


@login_required
def topics(request):
    """显示所有的主题"""
    # filter对用户限制，不是本用户创建的看不到
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  #根据创建时间来排序
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):  # topic_id来自于url中的(?P<topic_id>\d+)
    topic = Topic.objects.get(id=topic_id)  # /topic/5/
    if topic.owner != request.user:  # 保护单个条目的限制
        raise Http404
    # entry_set是在创建Entry model的外键才有的
    # 因为可能有多个条目所以order_by('date_added'),而且此时entries是个QuerySet是，
    #是一个列表，包含多个类的实例对象，每个对象都包含Entry中的属性字段topic,text,date_added
    #但是打印type(topic.entry_set)结果是learns.Entry.None,
    #>>> print(topic.entry_set)  --> learns.Entry.None
    #>>> type(topic.entry_set)
    #<class 'django.db.models.fields.related_descriptors.create_re....'
    entries = topic.entry_set.order_by('-date_added')   # 这里的entry_set指的是Entry.objects的一个内存对象，必须调用下面的方法，比如.all()和这里的
    #.order_by()方法才返回一个QuerySet是对象，topic想和对entry是one to many(一个topic对多个entry)
    context = {'topic': topic, 'entries': entries}  # 'topic'是变量将用于html中，topic是 #1下的topic对象
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':  # 不等于POST，就是GET
        form = TopicForm  # 不是POST,就初始化一个新的TopicForm类
    else:
        form = TopicForm(request.POST)  # 提交的数据再  request.POST下，然后实例化给form
        if form.is_valid():  # 检查数据是否合法，字段类型是否和models中定义的一样，有些必须要的参数是否为空等
            new_topic = form.save(commit=False)  # 如果commit=False的话，店家提交不会保存到数据库
            new_topic.owner = request.user  # 因为只用登陆才能创建主题，所以把此时请求创建的user给owner
            new_topic.save()
            form.save()  # 如果书据都有效，则吧书据保存在数据库
            # 用reverse获取目标url，HttpResponseRedirect则是跳转到获取的url页面
            # 逻辑上就是新建topic成功了，马上返回到topics.html页面，就会看到新增的topic
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}  # 把form 复制给form，form将在html中作为对象以{%%}的方式调用
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()  # get方法就返回空form到new_entry.html
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # 先不保存到数据库，暂时复制给new_entry
            new_entry.topic = topic  # 外键非空必须设置，这里没有下拉框选择，只能提前赋值，不然报错。还必须得是Topic中的某个
            # 之前我们添加entry的时候是在admin后台添加的，会有下拉框出现Topic中的字段(因为外键)
            # 而且用admin创建entry的topic字段时候如果你手动输入一个非Topic中text的字段(假设是‘mysql’)，
            # 会发现原来Topic自动增加一个mysql字段，然而这里没有下拉框选择，
            # 赋值来自于Topic的外键数据topic = Topic.objects.get(id=topic_id)
            new_entry.save()  # 保存到数据库
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        # >>> form --> <EntryForm bound=False, valid=Unknown, fields=(text)>
        form = EntryForm(instance=entry)  
        # instance参数获取的是EnteyForm中的filed的值
        # 也就是field=['text'],所以获取的就是条目的内容
    else:
        form = EntryForm(instance=entry, data=request.POST)  # data表示提交的内容
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
        """
            因为EntryForm中有model=Entry，所以form保存的时候需要知道是那个实例的对象，
        要么想上面一样实例化的时候加护当前实例对象EntryForm(instance=entry,data=request.POST)，
        或者想下面一样form.save(commit=False),再指定主键form.id =entry.id
        form = EntryForm(data=request.POST)  # data表示提交的内容
        if form.is_valid():
            form.save(commit=False)
            form.id =entry.id
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
        """

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request,'learning_logs/edit_entry.html', context)
