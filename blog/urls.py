#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/20 16:37
 
'''
from django.conf.urls import url

from . import views

# 网址和处理函数的关系
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 每一个页面对应一个url处理器
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # 配置归档路径下的文章
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view, name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
]

