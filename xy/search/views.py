from django.shortcuts import render
from .models import JobboleArticle
# Create your views here.

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# 主页视图函数
def IndexView(request):
    if request.method == 'GET':
        return render(request,'index.html')


# 搜素结果视图函数
def All_Results(request):
    if request.method == 'GET':
        articles = JobboleArticle.objects.all()[:80]
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(articles, 10,request=request)

        articles = p.page(page)
    context = {"articles":articles}
    return render(request,'all_results.html',context=context)