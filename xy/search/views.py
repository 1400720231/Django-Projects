from django.shortcuts import render
from .models import JobboleArticle
from django.db.models import Q
# Create your views here.

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# 主页视图函数
def IndexView(request):
    if request.method == 'GET':
        return render(request,'index.html')


# 搜素结果视图函数
def All_Results(request):
    if request.method == 'GET':
        articles = JobboleArticle.objects.all()

        sort = request.GET.get('sort', '') # 提取排序字段，默认为空
        if sort:# comment_nums　time
            if sort == 'praise_nums':
                articles = articles.order_by("-praise_nums")

        comment_nums = request.GET.get('comment_nums', '')
        if comment_nums:# comment_nums　time
            if comment_nums == 'comment_nums':
                articles = articles.order_by("-comment_nums")

        time = request.GET.get('time', '')
        if time:# comment_nums　time
            if time == 'create_date':
                articles = articles.order_by("-create_date")
        alls = request.GET.get('all', '')
        if alls:# comment_nums　time
            if time == 'create_date':
                articles = articles = JobboleArticle.objects.all()
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(articles, 10,request=request)

        articles = p.page(page)
    context = {"articles":articles,'comment_nums':comment_nums,'time':time,'sort':sort}
    return render(request,'all_results.html',context=context)





# 搜索视图函数
def SearchList(request):
    if request.method == 'GET':
        articles = JobboleArticle.objects.all()
        search_keywords = request.GET.get('keywords', "")  # 取不到默认为空
        if search_keywords:  # Q函数相当于or 的意思 要么name以keywors开头，要么desc 以keywords开头
            articles = articles.filter(
                Q(title__icontains=search_keywords) |
                Q(create_date__icontains=search_keywords)
                )
        sort = request.GET.get('sort', '')
        if sort:# comment_nums　time
            if sort == 'praise_nums':
                articles = articles.order_by("-praise_nums")

        comment_nums = request.GET.get('comment_nums', '')
        if comment_nums:# comment_nums　time
            if comment_nums == 'comment_nums':
                articles = articles.order_by("-comment_nums")

        time = request.GET.get('time', '')
        if time:# comment_nums　time
            if time == 'create_date':
                articles = articles.order_by("-create_date")
        alls = request.GET.get('all', '')
        if alls:# comment_nums　time
            if alls == 'create_date':
                articles = articles.filter(
                Q(title__icontains=search_keywords) |
                Q(create_date__icontains=search_keywords))
        try:  
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
    # Provide Paginator with the request object for complete querystring generation

        p = Paginator(articles, 10,request=request)

        articles = p.page(page)
    context = {"articles":articles, 'search_keywords': search_keywords,
                'sort':sort,'comment_nums':comment_nums,'time':time,'alls':alls}
    return render(request,'search_list.html',context=context)