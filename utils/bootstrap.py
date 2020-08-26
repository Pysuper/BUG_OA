# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : bootstrap
# Datetime : 2020/8/11 下午3:54


class BootStrapForm(object):
    """使用多继承完成每个Form添加HTML的动作"""

    bootstrap_class_exclude = []

    def __init__(self, *args, **kwargs):
        """重写父类的初始化方法，添加html标签"""
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():

            # 让每个继承它的类仍然可以自定义一些内容
            if name in self.bootstrap_class_exclude:
                continue

            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入{}".format(field.label)
