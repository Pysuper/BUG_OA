# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : wiki_forms
# Datetime : 2020/8/28 下午2:56


from .models import Wiki
from django import forms
from utils.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = Wiki
        exclude = ['project']  # 移除这个，显示其他的

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 找到想要的字段，把他绑定显示的数据重置
        total_data_list = [("", "请选择"),]
        data_list = Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_data_list.extend(data_list)

        self.fields["parent"].choices = total_data_list
