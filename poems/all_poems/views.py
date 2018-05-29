from django.shortcuts import render
from .models import Poems,Author
# 第三方分页插件
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.



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
    # 根据poem_id获取的目标诗词信息
    poem = Poems.objects.get(id=poem_id)
    author = Author.objects.get(id=poem.author_id)
    # 诗人所有诗词
    author_poems = author.poems_set.all()[:6]
    context = {'poem':poem,'author':author,'author_poems':author_poems}
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