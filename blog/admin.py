from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

    search_fields = ('title', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


# #  后台的评论管理器
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'post', 'created')
#     # list_filter = ()
#     search_fields = ('name', 'email', 'body')
#
#
# admin.site.register(Comment, CommentAdmin)
