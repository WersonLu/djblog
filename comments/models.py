from django.db import models

# Create your models here.
from django.db import models


# 储存评论
class Comment(models.Model):
    # 哪篇文章的评论
    post = models.ForeignKey('blog.Post')

    # 评论人的名字
    name = models.CharField(max_length=80)
    # 评论人邮箱
    email = models.EmailField()
    # 评论内容
    text = models.TextField()
    url = models.URLField(blank=True)
    # 评论时间
    created_time = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['created']

    def __str__(self):
        return self.text[:20]
