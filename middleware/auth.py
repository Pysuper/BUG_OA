# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 上午1:41
# @Author  : Zheng Xingtao
# @File    : auth.py
from datetime import datetime

from users.models import UserInfo
from django.shortcuts import redirect
from transac.models import Transaction, PricePolicy
from setting.base import WHITE_REGEX_URL_LIST
from django.utils.deprecation import MiddlewareMixin


class Tracer(object):
    """
    在中间件中封装tracer对象
    """

    def __init__(self):
        self.user = None
        self.price_policy = None


class AuthMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):

        # 实例化一个Tracer()对象
        request.tracer = Tracer()

        # 如果用户登录了, 在request中赋值
        user_id = request.session.get("user_id", 0)
        user_obj = UserInfo.objects.filter(id=user_id).first()

        request.tracer.user = user_obj

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

        if not request.tracer.user:
            return redirect('/user/login/user/')

        # 登录成功之后，进入后台管理时：获取当前用户所拥有的空间额度

        # 1. 免费额度在交易记录中存储
        # 获取用户ID值最大(最近的一次交易记录)
        _obj = Transaction.objects.filter(user=user_obj, status=2).order_by('-id').first()

        # # 判断当前用户的最后交易记录是否过期
        current_datetime = datetime.now()

        # # 如果交易记录存在，并且交易记录未过期
        # # 没有交易记录的时候，说明当前用户是免费版
        if _obj.end_datetime and _obj.end_datetime < current_datetime:
            # _obj = Transaction.objects.filter(user=user_obj, status=2).order('id').first()
            _obj = Transaction.objects.filter(user=user_obj, status=2, pro_policy__category=1).first()

        request.tracer.price_policy = _obj.pro_policy

        # 2. 免费额度存储在配置文件中
        """
        transaction_obj = Transaction.objects.filter(user=user_obj, status=2).order_by('-id').first()

        if not transaction_obj:
            # 没有购买
            request.price_policy = PricePolicy.objects.filter(category=1, title="个人免费版").first()
        else:
            # 付费版: 判断当前用户的最后交易记录是否过期
            current_datetime = datetime.now()
            if transaction_obj.end_datetime and transaction_obj.end_datetime < current_datetime:
                request.price_policy = PricePolicy.objects.filter(category=1, title="个人免费版").first()
            else:
                request.price_policy = transaction_obj.price_policy
        """
