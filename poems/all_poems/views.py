from django.shortcuts import render
from .models import Poems
# 第三方分页插件
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.



# 所有诗词展示视图函数
def All_Poems(request):
    all_poems = Poems.objects.all()
    poems = all_poems


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
    poem = Poems.objects.get(id=poem_id)
    context = {'poem':poem}
    return render(request,'poem_detail.html',context=context)