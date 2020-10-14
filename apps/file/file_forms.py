# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author   : Zheng Xingtao
# File     : file_forms.py
# Datetime : 2020/9/23 下午4:18


from django import forms
from django.core.exceptions import ValidationError

from utils.bootstrap import BootStrapForm
from utils.tencent.cos import check_file
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


class FileModelForm(forms.ModelForm):
    """
    验证用户上传的数据是否正确
    """
    etag = forms.CharField(label="ETag")  # 数据库中没有，在formModel中手动添加一个

    class Meta:
        model = FileRepository
        exclude = ['project', 'file_type', 'update_user', 'update_time']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_file_path(self):
        return "https://{}".format(self.cleaned_data["file_path"])

"""
这里先注释掉，影响效率
    def clean(self):
        # 主要完成数据信息校验，保证写入数据库时候的数据正确性
        key = self.cleaned_data["key"]
        etag = self.cleaned_data["etag"]
        size = self.cleaned_data["size"]
        if not key or not etag:
            return self.cleaned_data

        # 向COS校验文件是否合法(SDK的功能)
        from qcloud_cos.cos_exception import CosServiceError
        try:
            result = check_file(
                self.request.tracer.project.bucket,
                self.request.tracer.project.region,
                key
            )
        except CosServiceError as e:
            self.add_error("key", "文件上传未成功！")
            return self.cleaned_data

        # 校验ETag
        cos_etag = result.get("ETag")
        if etag != cos_etag:
            self.add_error("etag", "ETag错误")

        # 文件大小
        cos_length = result.get("Content-Length")
        if int(cos_length) != size:
            self.add_error("size", "文件大小错误！")

        return self.cleaned_data
"""