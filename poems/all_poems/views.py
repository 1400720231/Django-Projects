from django.shortcuts import render
from .models import Poems,Author
# 第三方分页插件
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from operation.forms import CommentsForm
from apps.yuyin import voice
import os
from operation.models import Praise
from django.db.models import Q



# 所有诗词展示视图函数
def All_Poems(request):
    all_poems = Poems.objects.all()
    poems = all_poems[0:30]


    # 分页插件
    try:
        page = request.GET.get('page',1)
    except PageNotAnInteger:
        page = 1
    # 这里的数字表示每一页有几个实例
    p = Paginator(all_poems, 5,request=request)
    all_poems = p.page(page)




    context ={'all_poems':all_poems,'poems':poems}
    return render(request,'all_poems.html',context=context)


# 某个诗词详情展示页面
def Poem_Detail(request,poem_id):
    comment_form = CommentsForm()
    # 根据poem_id获取的目标诗对象
    poem = Poems.objects.get(id=poem_id)
    author = Author.objects.get(id=poem.author_id)
    # 诗人所有诗词
    author_poems = author.poems_set.all()[:6]
    # 所以评论
    comments = poem.comments_set.all()
    # 评论数
    nums = comments.count()
    praise_num = Praise.objects.filter(poem=poem).count()
    try:
        page = request.GET.get('page',1)
    except PageNotAnInteger:
        page = 1
    # 这里的数字表示每一页有几个实例
    p = Paginator(comments, 4,request=request)
    comments = p.page(page)
    # 点赞状态标识
    praise_statue = 0
    if request.user.is_authenticated():
        statue = Praise.objects.filter(user=request.user,poem=poem)
        if statue:
            praise_statue=1
    #拼音功能
    result =[]
    temp =[]
    pingyin_statue = request.GET.get('pingyin_statue','')
    if pingyin_statue: 
        from xpinyin import Pinyin
        words = poem.content
       
        p = Pinyin()
        for i in words.split('\n'):
        # 生成拼音
            a = p.get_pinyin(i,show_tone_marks=True).split('-')
            for j in a:
                j = j+'&nbsp'*(6-len(j))
                temp.append(j)
            result.append(''.join(temp)+'\n')
            result.append(i+'\n')
            temp =[]

    context = {'poem':poem,'author':author,'author_poems':author_poems,
                'comments':comments,'comment_form':comment_form,
                'nums':nums,'praise_num':praise_num,'praise_statue':praise_statue,
                'result':result,'pingyin_statue':pingyin_statue}
    return render(request,'poem_detail.html',context=context)


# 所有诗人展示视图
def All_Poets(request):
    all_poets = Author.objects.all()

    # 分页插件
    try:
        page = request.GET.get('page',1)
    except PageNotAnInteger:
        page = 1
    # 这里的数字表示每一页有几个实例
    p = Paginator(all_poets, 5,request=request)
    all_poets = p.page(page)

    poems=Poems.objects.all()[:20]
    context = {'all_poets':all_poets,'poems':poems}
    return render(request,'all_poets.html',context=context)

# 某个诗人详情展示页面
def Poet(request,poet_id):

    # 获取目标诗人实例对象
    poet = Author.objects.get(id=poet_id)
    # 获取他所有诗集
    all_poems = poet.poems_set.all()[:20]

    poems = Poems.objects.all()[0:20]
    # 分页插件
    try:
        page = request.GET.get('page',1)
    except PageNotAnInteger:
        page = 1
    # 这里的数字表示每一页有几个实例
    p = Paginator(all_poems, 3,request=request)
    all_poems = p.page(page)

    context = {'poet':poet,'all_poems':all_poems,'poems':poems}
    return render(request,'poet_detail.html',context=context)

# 声音播放
@require_POST
@csrf_exempt
def Voice(request):
    poem_id = request.POST.get('id')
    poem = Poems.objects.get(id=poem_id)
    title = poem.title
    content = poem.content
    # 获取语音链接
    order = voice(title,content)
    # 利用os模块执行语音链接来实现语音播报
    os.system(order)
    return HttpResponse('1')


# 搜索视图函数
def SearchList(request):
    if request.method == 'GET':
        # 生成日志保存在数据库中
        all_poems = Poems.objects.all()
        poems = all_poems[:30]
        search_keywords = request.GET.get('keywords', "")  # 取不到默认为

        if search_keywords:  # Q函数相当于or 的意思 要么name以keywors开头，要么desc 以keywords开头
            all_poems = all_poems.filter(
                #　搜索诗词标题
                Q(title__icontains=search_keywords) |
                # 搜索标签
                Q(tag__icontains=search_keywords)|
                # 搜索作者
                Q(author__name__icontains=search_keywords)|
                # 作品集搜索
                Q(collection__icontains=search_keywords)|
                # 内容搜索
                Q(content__icontains=search_keywords))        
        try:  
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
    # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_poems, 6,request=request)
        all_poems = p.page(page)
        context ={'all_poems':all_poems,'poems':poems}
        return render(request,'all_poems.html',context=context)


