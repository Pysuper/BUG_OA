from .models import Project, ProjectUser
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from .project_forms import ProjectModelForm


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
                project_dict["star"].append(row)
            else:
                project_dict["my"].append(row)

        for item in my_join_list:
            if item.star:
                project_dict["star"].append(item.project)
            else:
                project_dict["my"].append(item.project)

        return render(request, "project/project_list.html", {"form": form, "project_dict": project_dict})

    def post(self, request):
        form = ProjectModelForm(request, data=request.POST)
        if form.is_valid():
            # 验证通过：项目名、颜色、描述 + 谁创建的项目(creator)
            form.instance.creator = request.tracer.user  # 当前登录的用户
            form.save()  # 创建项目

            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": form.errors})
