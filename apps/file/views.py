from django.http import JsonResponse
from django.shortcuts import render

from .file_forms import FolderModelForm
from .models import FileRepository


# Create your views here.


def file(request, project_id):
    # 处理parent_id
    parent_obj = None
    folder_id = request.GET.get("folder", "")
    if folder_id.isdecimal():
        parent_obj = FileRepository.objects.filter(
            id=int(folder_id),
            file_type=2,
            project=request.tracer.project
        ).first()

    # 文件列表
    if request.method == "GET":
        form = FolderModelForm(request, parent_obj)
        return render(request, 'manages/file/file.html', {'form': form})

    # 添加文件夹 --> 上传到已有的文件夹中
    form = FolderModelForm(request, parent_obj, data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_obj
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
