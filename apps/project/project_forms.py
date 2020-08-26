# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : project_forms
# Datetime : 2020/8/24 下午4:42


from django import forms
from project.models import Project
from utils.bootstrap import BootStrapForm
from utils.widgets import ColorRadioSelect
from django.core.exceptions import ValidationError


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ["color"]

    # desc = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Project
        fields = ["name", "color", "desc"]
        widgets = {
            "desc": forms.Textarea,
            "color": ColorRadioSelect   # TODO: 这里找不到指定渲染的模板文件
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """项目校验"""
        name = self.cleaned_data["name"]

        # 当前登录的用户
        current_user = self.request.tracer.user

        # 1. 当前用户是否已创建过此项目(项目名是否存在)
        exists = Project.objects.filter(name=name, creator=current_user).exists()
        if exists:
            raise ValidationError("项目名已存在！")

        # 2， 当前用户是否还有额度创建项目
        # 最多能创建的个数
        most_num = self.request.tracer.price_policy.project_num

        # 现在已创建的项目个数
        # 可以用户中添加一个字段，这样就不需要每次查询了
        now_count = Project.objects.filter(creator=current_user).count()

        if now_count >= most_num:
            raise ValidationError("项目个数已超限，请购买套餐！")

        return name
