from django.shortcuts import render

# Create your views here.

import markdown
from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.db.models import Q
# q对象,查询表达式
# 改写类视图函数
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail


# request 是django封装好的http请求,返回一个http响应给用户
class IndexView(ListView):
    # 我要获取的模型是post
    model = Post
    template_name = 'blog/index.html'
    # 这个变量会传递给模板
    context_object_name = 'post_list'
    paginate_by = 3


# def index(request):
#     # return HttpResponse("欢迎")
#     # 以时间倒序查询文章,存在变量里
#     post_list = Post.objects.all().order_by('-created_time')
#     # return render(request, 'blog/index.html', context={
#     #     'title': '我的博客',
#     #     'welcome': '欢迎光临'
#     # })
#     # post_list=Post.objects.filter(created_time__year=year,
#     #                               created_time__month=month).order_by('-created_time')
#
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list
#     })


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


#
# class ArchivesView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#
#     def get_queryset(self):
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
#                                                    created_time__month=month)
# 详情页的类视图函数写法,但是没有引用
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])
        post.body = md.convert(post.body)
        post.toc = md.toc

        return post

    # 显示评论数据的方法
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # form=
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 每次触发detail函数,就调用阅读增加方法
    post.increase_views()
    # markdown 语法拓展
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()

    return render(request, 'blog/detail.html', context={'post': post,
                                                        'form': form,
                                                        'comment_list': comment_list})


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    # 获取搜索框的值
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键字'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    # 数据库包含过滤查询
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})


# 分享
def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk)
    sent = ''
    recipient = ''
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({})recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'],
                                                                     cd['comments'])
            send_mail(subject, message, 'wersonlau@163.com', [cd['to']])
            recipient = cd['to']
            sent = True
    else:
        form = EmailPostForm()
        recipient = False
    return render(request, 'blog/share.html',
                  {
                      'post': post,
                      'form': form,
                      'sent': sent,
                      'recipient': recipient}
                  )


def contact(request):
    return render(request, 'blog/contact.html', context={
        'welcome': '足下的到访使小站蓬荜生辉'
    })
