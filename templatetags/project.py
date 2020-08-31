# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : project_tags
# Datetime : 2020/8/27 下午5:17


from django.urls import reverse
from django.template import Library
from project.models import Project, ProjectUser

register = Library()


@register.inclusion_tag('project/all_project_list.html')
def all_project_list(request):
    # 1. 获我创建的所有项目
    my_project_list = Project.objects.filter(creator=request.tracer.user)

    # 2. 获我参与的所有项目
    join_project_list = ProjectUser.objects.filter(user=request.tracer.user)

    return {'my': my_project_list, 'join': join_project_list, 'request': request}


@register.inclusion_tag('project/manage_menu_list.html')
def manage_menu_list(request):
    project_id = request.tracer.project.id
    data_list = [
        {
            "title": "概述",
            "url": reverse("manages:dashboard", kwargs={"project_id": project_id})
        }, {
            "title": "问题",
            "url": reverse("manages:issues", kwargs={"project_id": project_id})
        }, {
            "title": "统计",
            "url": reverse("manages:statistics", kwargs={"project_id": project_id})
        }, {
            "title": "文件",
            "url": reverse("manages:file", kwargs={"project_id": project_id})
        }, {
            "title": "WiKi",
            "url": reverse("manages:wiki:home", kwargs={"project_id": project_id})
        }, {
            "title": "设置",
            "url": reverse("manages:setting", kwargs={"project_id": project_id})
        },
    ]

    for item in data_list:
        if request.path_info.startswith(item["url"]):
            item["class"] = "active"

    return {"data_list": data_list}
