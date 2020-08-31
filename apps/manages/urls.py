# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : urls
# Datetime : 2020/8/27 下午6:32


from .views import *
from django.urls import include
from django.conf.urls import url

urlpatterns = [
    url(r'dashboard', dashboard, name="dashboard"),
    url(r'issues', issues, name="issues"),
    url(r'statistics', statistics, name="statistics"),
    url(r'file', file, name="file"),
    url(r'^wiki/', include(('wiki.urls', "wiki"))),  # 再做一次路由分发
    url(r'setting', setting, name="setting"),
]
