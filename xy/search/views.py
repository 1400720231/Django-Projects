from django.shortcuts import render,reverse
from .models import JobboleArticle
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
# Create your views here.
from operation.models import LogMessage
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import json

# 主页视图函数
def IndexView(request):
    if request.method == 'GET':
        hots = LogMessage.objects.all().order_by('-times')[:4]

        context = {'hots':hots}
        return render(request,'index.html',context=context)


# 所有结果视图函数
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
        # 生成日志保存在数据库中
        articles = JobboleArticle.objects.all()
        search_keywords = request.GET.get('keywords', "")  # 取不到默认为空
        
        # 有输入的内容就保存在数据库
        if search_keywords:
            try: # 如果已经存在,就查询次数+1
                exist_log = LogMessage.objects.get(history=search_keywords)
                exist_log.times +=1
                exist_log.save()
            except Exception as e: # 不存在,就实例化一个
                log = LogMessage()
                log.history = search_keywords
                log.times =1
                log.save()
        else:  # 如果没有输入内容就直接回index页面
            return HttpResponseRedirect(reverse('index'))

        if search_keywords:  # Q函数相当于or 的意思 要么name以keywors开头，要么desc 以keywords开头
            articles = articles.filter(
                Q(title__icontains=search_keywords) |
                Q(create_date__icontains=search_keywords))

        # 历史搜索填充函数
        historys = LogMessage.objects.all().order_by('-date')[:10]
        count = articles.count()



        # 排序整理
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
                'sort':sort,'comment_nums':comment_nums,'time':time,'alls':alls,
                'historys':historys,'count':count}
    return render(request,'search_list.html',context=context)


# 智能提示视图函数
def suggest(request):
    if request.method == 'GET':
        keywords = request.GET.get('keywords','')
     
        articles = JobboleArticle.objects.all()  # 全部queryset对象
        data = articles.filter(title__icontains=keywords)[:5] # 查询匹配语句
        result = []
        for i in data:
            result.append(i.title)
    return HttpResponse(json.dumps(result), content_type ='application/json')