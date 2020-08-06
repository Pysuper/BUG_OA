# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : develop.py
# Datetime : 2020/8/5 下午2:39

import os, sys
from .base import *

ALLOWED_HOSTS = ["*", ]

# 使用中文
LANGUAGE_CODE = 'zh-hans'

# 配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root',
        'NAME': 'debug',
    }
}
# 短信配置
SMS_TEMPLATES = {
    "register": "682840",
    "login": "682843",
    "update": "682844",
    "love": "683020"
}

TENCENT_SMS_APPID = 1400407994
TENCENT_SMS_APPKEY = "0dd1c9e4004fe503700c08d4e4d5098"
TENCENT_SMS_SIGN = "郑兴涛个人公众号"

# 模板文件
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 配置静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))