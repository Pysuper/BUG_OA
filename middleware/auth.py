# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 上午1:41
# @Author  : Zheng Xingtao
# @File    : auth.py


from datetime import datetime
from users.models import UserInfo
from django.shortcuts import redirect
from transac.models import Transaction
from setting.base import WHITE_REGEX_URL_LIST
from project.models import Project, ProjectUser
from django.utils.deprecation import MiddlewareMixin


class Tracer(object):
    """
    在中间件中封装tracer对象
    """

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):
    """
    用户校验的中间件
    1. process_request
    2. process_view
    """

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

    @staticmethod
    def process_view(request, view, args, kwargs):
        # 判断URL是否是以manage开头
        if not request.path_info.startswith("/manage/"):
            return

        # 如果是则判断项目是否是我自己的项目 or 参与
        project_id = kwargs.get("project_id")
        project_obj = Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_obj:
            request.tracer.project = project_obj
            return  # 是我创建的项目，通过

        # 是否是我参与的项目
        project_user_obj = ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_obj:
            request.tracer.project = project_user_obj.project
            return  # 是我参加的项目

        return redirect('/project/list/')
