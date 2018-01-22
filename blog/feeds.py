#!/usr/bin/env python

# encoding: utf-8

'''
 
@author: wersonliu

@contact: wersonliugmail.com
 
@time: 2018/1/22 18:09
 
'''

from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    title = "Django博客"
    link = "/"
    description = "Django博客文章"

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s]%s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
