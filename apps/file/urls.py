# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author   : Zheng Xingtao
# File     : urls.py
# Datetime : 2020/9/23 下午4:18


from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', file, name="home"),
    url(r'^delete/$', file_delete, name="delete"),
]
