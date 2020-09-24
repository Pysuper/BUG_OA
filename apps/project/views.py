from time import time
from .models import Project, ProjectUser
from django.views.generic.base import View
from rest_framework.viewsets import ViewSet
from utils.tencent.cos import create_bucket
from .project_forms import ProjectModelForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from setting.variable import TENCENT_COS_REGION, TENCENT_COS_API_KEY_ID


# Create your views here.
class ProjectInfo(View):
    def get(self, request):
        form = ProjectModelForm(request)

        # 获取我创建，我参与的项目
        project_dict = {"star": [], "my": [], "join": []}
        my_project_list = Project.objects.filter(creator=request.tracer.user)
        my_join_list = ProjectUser.objects.filter(user=request.tracer.user)

        for row in my_project_list:
            if row.star:
                project_dict["star"].append({"value": row, "type": "my"})
            else:
                project_dict["my"].append({"value": row, "type": "join"})

        for item in my_join_list:
            if item.star:
                project_dict["star"].append(item.project)
            else:
                project_dict["my"].append(item.project)

        return render(request, "project/project_list.html", {"form": form, "project_dict": project_dict})

    def post(self, request):
        form = ProjectModelForm(request, data=request.POST)
        if form.is_valid():
            # 1. 为每个项目创建一个桶 --> 并为桶创建跨域规则

            bucket = "{}-{}".format(request.tracer.user.phone, str(int(time()))) + TENCENT_COS_API_KEY_ID
            create_bucket(TENCENT_COS_REGION, bucket)

            # 2. 把桶和区域写入到数据库
            form.instance.bucket = bucket
            form.instance.region = TENCENT_COS_REGION

            # 验证通过：项目名、颜色、描述 + 谁创建的项目(creator)
            form.instance.creator = request.tracer.user  # 当前登录的用户
            form.save()  # 创建项目

            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": form.errors})


class ProjectStar(ViewSet):
    """这里直接使用类视图的方法，获取当前用户的星标操作"""

    def add_star(self, request, project_type, project_id):
        """
        添加星标的动作
        :param request: request请求对象
        :param project_type: 前端发送的Project的类型：my、join、
        :param project_id: 用户点击的Project_id
        :return: 项目列表的页面
        """
        if project_type == "my":
            Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
            return redirect("/project/list/")

        elif project_type == "join":
            ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
            return redirect("/project/list/")

        return HttpResponse("请求失败...！")

    def delete_star(self, request, project_type, project_id):
        """在这里我们需要区分：我创建、我参与"""
        if project_type == "my":
            Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
            return redirect("/project/list/")

        elif project_type == "join":
            ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
            return redirect("/project/list/")

        return HttpResponse("请求失败...！")
