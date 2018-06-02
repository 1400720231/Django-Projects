from django.shortcuts import render
from .forms import CommentsForm,PraiseForm
from all_poems.models import Poems
from operation.models import Comments
# Create your views here.
from django.shortcuts import render
from django.shortcuts import reverse
# Create your views here.
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from operation.models import Praise


#　评论视图函数
@login_required(login_url='/user/login/')
def Comments(request,poem_id):
    if request.method =='POST':
        # 评论的诗词
        poem = Poems.objects.get(id=poem_id)
        form = CommentsForm(request.POST)
        # modelform类型表单，需要commit=false才能对属性赋值
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.poem = poem
            new_form.save()
    return HttpResponseRedirect(reverse('all_poems:poem_detail',args=[poem_id]))

#点赞

@csrf_exempt
@login_required(login_url='/user/login/')
def Praise_poems(request,poem_id):

    poem = Poems.objects.get(id=poem_id)
    # 判断是否已经点赞过
    statue = Praise.objects.filter(user=request.user,poem=poem)
    if statue:
        ins = Praise.objects.get(user=request.user,poem=poem)
        ins.delete()
    else:
        form = PraiseForm()
        new_form = form.save(commit=False)
        new_form.poem = poem
        new_form.user = request.user
        new_form.save()
    return HttpResponseRedirect(reverse('all_poems:poem_detail',args=[poem_id]))

