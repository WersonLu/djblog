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
urlpatterns = [
    url(r'^$', views.index, name='index')
]
