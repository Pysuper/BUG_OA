# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 上午1:06
# @Author  : Zheng Xingtao
# @File    : urls.py.py

from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^logout/$', logout, name="logout"),
    url(r'^sms/$', send_sms, name="send_sms"),
    url(r'^image/code/$', image_code, name="image_code"),
    url(r'^register/$', Register.as_view(), name="register"),
    url(r'^login/sms/$', LoginSms.as_view(), name="login_sms"),
    url(r'^login/user/$', LoginUser.as_view(), name="login_user"),
]
