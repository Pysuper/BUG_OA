from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views.generic.base import View
from utils.tencent.cos import delete_bucket
from project.models import Project

# Create your views here.
def instal(request, project_id):
    return render(request, 'manages/instal/setting.html')


class Delete(View):
    def get(self, request, project_id):
        return render(request, 'manages/instal/delete.html')

    def post(self, request, project_id):
        project_name = request.POST.get("project_name")
        if not project_name or project_name != request.tracer.project.name:
            return render(request, 'manages/instal/delete.html', {"error": "项目名错误！"})

        # 这时候说明项目名是正确的
        if request.tracer.user != request.tracer.project.creator:
            return render(request, 'manages/instal/delete.html', {"error": "只有项目创建者可以删除项目"})

        """
        创建者执行删除:
            - 删除桶：
                - 找到并删除桶中的所有文件
                - 找到并删除桶中的所有碎片
                - 删除桶
            - 删除项目
        """
        delete_bucket(request.tracer.project.bucket, request.tracer.project.region)
        Project.objects.filter(id=request.tracer.project.id).delete()
        return redirect("project:list")
