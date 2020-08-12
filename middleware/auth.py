# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 上午1:41
# @Author  : Zheng Xingtao
# @File    : auth.py

from users.models import UserInfo
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        # 如果用户登录了, 在request中赋值
        user_id = request.session.get("user_id", 0)
        user_obj = UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_obj
