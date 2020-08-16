# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/16 下午4:39
# @Author  : Zheng Xingtao
# @File    : init_price_policy.py


import script_base
from transac.models import PricePolicy


def init_run():
    exists = PricePolicy.objects.filter(category=1, title="个人免费版").exists()

    if not exists:
        PricePolicy.objects.create(
            category=1,
            title="个人免费版",
            price=0,
            project_num=3,
            project_member=2,
            project_space=20,
            per_file_size=5,  # 注意文件字节的转换关系
        )


if __name__ == '__main__':
    init_run()
