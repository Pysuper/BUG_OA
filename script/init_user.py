# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 下午10:11
# @Author  : Zheng Xingtao
# @File    : init_user.py


import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setting.develop")
django.setup()

# 在导入配置文件之后导入模型类
from users.models import UserInfo

UserInfo.objects.create(username="zheng", password="qwe123123", phone=18111111113, email="123123123@qq.com")
