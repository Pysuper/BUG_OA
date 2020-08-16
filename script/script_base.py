# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/16 下午4:45
# @Author  : Zheng Xingtao
# @File    : base.py


import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setting.develop")
django.setup()
