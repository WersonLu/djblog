#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/22 16:22
 
'''
from .models import Comment


class CommentForm():
    class Meta:
        model = Comment
        # 用户填写的三个字段
        fields = ('name', 'email', 'body')
