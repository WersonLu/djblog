#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/23 17:46
 
'''
from blog.models import Post
from blog.api.serializers import PostSerializer

post = Post.objects.all()
serializer = PostSerializer(Post)
serializer.data
