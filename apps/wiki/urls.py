# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : urls
# Datetime : 2020/8/28 上午11:21


from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', wiki, name="home"),  # 再做一次路由分发
    url(r'add/$', AddWiki.as_view(), name="add"),
    url(r'catalog/$', catalog, name="catalog"),
    url(r'delete/(?P<wiki_id>\d+)/$', delete_wiki, name="delete"),
    url(r'edit/(?P<wiki_id>\d+)/$', edit_wiki, name="edit"),
]