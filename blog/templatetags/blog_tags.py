#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/22 12:18
 
'''
from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()


# 最近文章标签注册
@register.simple_tag
def get_recent_posts(num=5):
    # 获取数据库中的前五篇文章
    return Post.objects.all().order_by('-created_time')[:num]


# 归档标签注册
@register.simple_tag
def archives():
    return Post.objects.all().dates('created_time', 'month', order='DESC')


# 分类标签注册
@register.simple_tag
def get_categories():
    # return Category.objects.all()
    # 使用annotate 统计数量
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 获取标签
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
