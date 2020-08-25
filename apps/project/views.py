from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .project_forms import ProjectModelForm


# Create your views here.
class ProjectInfo(View):
    def get(self, request):
        form = ProjectModelForm(request)
        return render(request, "project/project_list.html", {"form": form})

    def post(self, request):
        form = ProjectModelForm(request, data=request.POST)
        if form.is_valid():
            # 验证通过：项目名、颜色、描述 + 谁创建的项目(creator)
            form.instance.creator = request.tracer.user  # 当前登录的用户
            form.save()  # 创建项目

            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": form.errors})
