# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author   : Zheng Xingtao
# File     : file_forms.py
# Datetime : 2020/9/23 下午4:18


from django import forms
from django.core.exceptions import ValidationError

from utils.bootstrap import BootStrapForm
from .models import FileRepository


class FolderModelForm(BootStrapForm, forms.ModelForm):
    """文件夹的ModelForm"""

    class Meta:
        model = FileRepository
        fields = ['name']

    def __init__(self, request, parent_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent_obj = parent_obj

    def clean_name(self):
        name = self.cleaned_data["name"]

        # 判断当前目录下，此文件夹是否存在
        query_set = FileRepository.objects.filter(file_type=2, name=name, project=self.request.tracer.project)

        # 判断当前目录下，此文家是否存在
        # query_set = FileRepository.objects.filter(name=name, project=self.request.tracer.project)

        if self.parent_obj:
            exists = query_set.filter(parent__isnull=self.parent_obj).exists()
        else:
            exists = query_set.filter(parent__isnull=True).exists()

        if exists:
            raise ValidationError("文件夹已存在")
        return name
