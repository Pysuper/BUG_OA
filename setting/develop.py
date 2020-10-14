# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : develop.py
# Datetime : 2020/8/5 下午2:39

import sys
from .base import *
import utils.log_theme

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
                'django.template.context_processors.media',
            ],
            'libraries': {
                'project': 'templatetags.project'
            }
        },
    },
]

CACHES = {  # 可以使用不同的配置，实现读写分离
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://0.0.0.0:6379/0",  # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "root"  # redis密码
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middleware.auth.AuthMiddleware'  # 手动实现中间件
]

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 配置静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 图片验证码中字体文件的路径
TTF_PATH = os.path.join(BASE_DIR, 'static/ttf/')

# 项目颜色选择
COLOR_CHOICES = (
    (1, "#56b8eb"),  # 56b8eb
    (2, "#f28033"),  # f28033
    (3, "#ebc656"),  # ebc656
    (4, "#a2d148"),  # a2d148
    (5, "#20BFA4"),  # #20BFA4
    (6, "#7461c2"),  # 7461c2,
    (7, "#20bfa3"),  # 20bfa3,
)

# CORS
CORS_ORIGIN_WHITELIST = ('127.0.0.1:8090', 'localhost:8090', '0.0.0.0:8090',)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# 日志信息
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/cms.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}


try:
    from .variable import *
except:
    pass