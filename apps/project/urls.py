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


"""
如果不创建单独的app，url设计
url(r'manage/(?P(<project_id>\d+)/', include([
    url(r'dashboard', dashboard, name="manage_dashboard"),
    url(r'issues', issues, name="manage_issues"),
    url(r'statistics', statistics, name="manage_statistics"),
    url(r'file', file, name="manage_file"),
    url(r'wiki', wiki, name="manage_wiki"),
    url(r'setting', setting, name="manage_setting"),
], None)
"""