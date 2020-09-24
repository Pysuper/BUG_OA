# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : urls
# Datetime : 2020/8/27 下午6:32


from .views import *
from django.urls import include
from django.conf.urls import url

# 再做一次路由分发
urlpatterns = [
    url(r'^board/', include(('board.urls', "dashboard"))),
    url(r'^issues/', include(('matter.urls', "issues"))),
    url(r'^statistics/', include(('count.urls', "statistics"))),
    url(r'^wiki/', include(('wiki.urls', "wiki"))),
    url(r'^file/', include(('file.urls', "file"))),
    url(r'^setting/', include(('instal.urls', "setting"))),
]
