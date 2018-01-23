#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/23 17:52
 
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^posts/$', views.PostListView.as_view(), name='post_list'),
    url(r'^posts/(?P<pk>\d+)/$', views.PostDetailView.as_view(),
        name='post_detail')
]
