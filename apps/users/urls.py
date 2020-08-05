# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 上午1:06
# @Author  : Zheng Xingtao
# @File    : urls.py.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'sms/$', send_sms),
]
