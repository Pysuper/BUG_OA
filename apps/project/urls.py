# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/16 下午5:25
# @Author  : Zheng Xingtao
# @File    : urls.py


from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', project_list, name="list"),

]
