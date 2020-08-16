# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 上午1:41
# @Author  : Zheng Xingtao
# @File    : auth.py
from datetime import datetime

from django.shortcuts import redirect
from transac.models import Transacation
from users.models import UserInfo
from setting.base import WHITE_REGEX_URL_LIST
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        # 如果用户登录了, 在request中赋值
        user_id = request.session.get("user_id", 0)
        user_obj = UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_obj

        # 白名单：用户没有登录都可以访问的页面
        """
        1. 获取当前访问的url
        2. 判断url是否在白名单中
            2.1 在--继续向后访问
            2.2 不在--判断时候已登录
                2.2.1 已登录--继续向后访问
                2.2.2 未登录--返回登录页面
        """

        if request.path_info in WHITE_REGEX_URL_LIST:
            return

        if not request.tracer:
            return redirect('/user/login/user/')

        # 登录成功之后，进入后台管理时：获取当前用户所拥有的空间额度
        # 1. 免费额度在交易记录中存储
        # 2. 免费额度存储在配置文件中

        # 获取用户ID值最大(最近的一次交易记录)
        transaca_obj = Transacation.objects.filter(user=user_obj, status=2).order('-id').first()

        # 判断当前用户的最后交易记录是否过期
        crrent_datetime = datetime.now()

        # 如果交易记录存在，并且交易记录未过期
        # 没有交易记录的时候，说明当前用户是免费版
        if transaca_obj.end_datetime and transaca_obj.end_datetime < crrent_datetime:
            # transaca_obj = Transacation.objects.filter(user=user_obj, status=2).order('id').first()
            transaca_obj = Transacation.objects.filter(user=user_obj, status=2, price_policy__category=1).first()
        request.transaca = transaca_obj
