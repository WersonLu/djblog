from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post


# request 是django封装好的http请求,返回一个http响应给用户
def index(request):
    # return HttpResponse("欢迎")
    # 以时间倒序查询文章,存在变量里
    post_list = Post.objects.all().order_by('-created_time')
    # return render(request, 'blog/index.html', context={
    #     'title': '我的博客',
    #     'welcome': '欢迎光临'
    # })
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.index', context={'post': post})
