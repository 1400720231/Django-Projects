from django.shortcuts import render

# Create your views here.
from .models import BlogArticles


def blog_title(request):
	blogs = BlogArticles.objects.all()
	context = {"blogs":blogs}
	return render(request, 'titles.html', context=context)