# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 上午1:06
# @Author  : Zheng Xingtao
# @File    : urls.py.py

from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^sms/$', send_sms),
    url(r'^register/$', Register.as_view(), name="register"),
    url(r'^login/sms/$', LoginSms.as_view(), name="login_sms")
]
