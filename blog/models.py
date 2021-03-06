from django.db import models

# Create your models here.
# blog/models.py
import markdown
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
# from django.core.urlresolvers import reverse
from django.urls import reverse

# api拓展
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


# 创建文章,标签等模型
class Category(models.Model):
    """
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    Django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 使用摘要还有第二种方法  truncatechares模板过滤器
    def save(self, *args, **kwargs):
        # 如果没有摘要,从文本主题截取54个字符赋给excerpt
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。

    # 一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是
    # ForeignKey，即一对多的关联关系。
    category = models.ForeignKey(Category)
    # 1篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
    # ManyToManyField，表明这是多对多的关联关系,文章可以没有标签
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.PositiveIntegerField(default=0)
    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 排序属性
    class Meta:
        ordering = ['-created_time']

    # 增加文章阅读数的方法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

# # 储存评论
# class Comment(models.Model):
#     # 哪篇文章的评论
#     post = models.ForeignKey(Post, related_name='comments')
#     # 评论人的名字
#     name = models.CharField(max_length=80)
#     # 评论人邮箱
#     email = models.EmailField()
#     # 评论内容
#     body = models.TextField()
#     # 评论时间
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['created']
#
#     def __str__(self):
#         return 'Comment by {} on {}'.format(self.name, self.post)
