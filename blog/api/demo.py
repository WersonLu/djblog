#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/23 17:46
 
'''
from blog.models import Post
from blog.api.serializers import PostSerializer
from blog.serializers import PostSerializer
post = Post.objects.latest('pk')
serializer = PostSerializer(Post)
serializer = PostSerializer()
serializer.data

print(repr(serializer))


