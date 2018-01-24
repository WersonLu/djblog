#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/24 12:44
 
'''
from django.conf.urls import url
from . import views

app_name = 'account'
urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
]
