# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author   : Zheng Xingtao
# File     : get_image.py
# Datetime : 2020/10/21 上午9:49

import requests

res = requests.get("url")
print(res.content)