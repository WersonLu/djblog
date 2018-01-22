from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    # 获取文章,不存在返回404
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        # 类字典对象,request.post 储存用户评论
        form = CommentForm(request.POST)
        # 检测表单数据格式是否正确
        if form.is_valid():
            # commit = False
            # 的作用是仅仅利用表单的数据生成
            # Comment
            # 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            # 关联
            comment.post = post
            comment.save()
            # 重定向,调用get_absolute_url返回绝对路径
            return redirect(post)
        else:
            # 数据格式不正确,
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    # 重定向,调用get_absolute_url返回绝对路径
    return redirect(post)
