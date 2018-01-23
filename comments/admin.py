from django.contrib import admin

# Register your models here.
from .models import Comment


# 后台评论管理系统
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'url', 'text', 'created_time', 'post')
    search_fields = ('name', 'email', 'text')


admin.site.register(Comment, CommentAdmin)
