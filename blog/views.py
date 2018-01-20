from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render


# request 是django封装好的http请求,返回一个http响应给用户
def index(request):
    # return HttpResponse("欢迎")
    return render(request, 'blog/index.html', context={
        'title': '我的博客',
        'welcome': '欢迎光临'
    })
