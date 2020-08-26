# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/16 下午5:25
# @Author  : Zheng Xingtao
# @File    : urls.py


from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', ProjectInfo.as_view(), name="list"),
    url(r'add_star/(?P<project_type>\w+)(?P<project_id>\d+)/$', ProjectStar.as_view({"get": "add_star"}), name="add_star"),
    url(r'delete_star/(?P<project_type>\w+)(?P<project_id>\d+)/$', ProjectStar.as_view({"get": "delete_star"}), name="delete_star"),

]
