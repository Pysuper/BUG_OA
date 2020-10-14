import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from setting.variable import TENCENT_COS_REGION
from utils.tencent.cos import delete_file, delete_file_list, credential
from .file_forms import FolderModelForm, FileModelForm
from .models import FileRepository

# Create your views here.
"""View APIView ViewSet"""


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

    # GET 文件列表
    if request.method == "GET":
        # 导航栏
        breadcrumb_list = []
        parent = parent_obj
        while parent:
            # breadcrumb_list.insert(0, {"id": parent.id, "name": parent.name})
            breadcrumb_list.insert(0, model_to_dict(parent, ["id", "name"]))
            parent = parent.parent

        # 当前目录下的所有文件、文件夹获取到
        query_set = FileRepository.objects.filter(project=request.tracer.project).order_by('-file_type')
        if query_set:
            file_obj_list = query_set.filter(parent=parent_obj)
        else:
            file_obj_list = query_set.filter(parent__isnull=True)

        form = FolderModelForm(request, parent_obj)
        return render(
            request, 'manages/file/file.html',
            {
                "form": form,
                "file_obj_list": file_obj_list,
                "breadcrumb_list": breadcrumb_list,
                "folder_obj": parent_obj,  # 当前访问的文件目录
            }
        )

    # POST 添加文件夹 & 文件夹修改 --> 上传到已有的文件夹中
    # 文件夹修改
    fid = request.POST.get("fid")
    edit_obj = None
    if fid.isdecimal():
        edit_obj = FileRepository.objects.filter(
            id=int(fid),
            file_type=2,
            project=request.tracer.project
        ).first()

    if edit_obj:
        form = FolderModelForm(request, parent_obj, data=request.POST, instance=edit_obj)
    else:
        form = FolderModelForm(request, parent_obj, data=request.POST)

    # 新建文件夹
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_obj
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def file_delete(request, project_id):
    """删除文件"""
    fid = request.GET.get("fid")

    # 删除数据库中文件和文件夹的信息，级联删除
    delete_obj = FileRepository.objects.filter(id=fid, project=request.tracer.project).first()

    # 同时删除桶中的信息
    if delete_obj.file_type == 1:
        # 文件 --> 数据库删除，cos文件删除，项目已使用的空间容量返还

        # 删除文件，将容量还给当前项目的已使用空间
        request.tarcer.project.user_space -= delete_obj.file_size
        request.tracer.project.save()

        # COS中删除文件
        delete_file(request.tracer.project.bucket, TENCENT_COS_REGION, delete_obj.key)

        # 数据库中删除记录
        delete_obj.delete()

    # 文件夹 --> 找到当前文件夹中的所有文件 --> （数据库删除，cos文件删除，项目已使用的空间容量返还）
    # 反向查询？！递归修改数据
    total_size = 0
    key_list = []
    folder_list = [delete_obj, ]
    for folder in folder_list:
        child_list = FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by('-file_type')
        for child in child_list:  # 遍历文件和文件夹
            if child.file_type == 2:
                folder_list.append(child)
            else:
                # 这个时候-->处理文件
                total_size += child.file_type
                # delete_file(request.tracer.project.bucket, request.tracer.project.region, child.key)
                key_list.append({"Key": child.key})

    # COS批量删除文件
    if key_list:
        delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)

    # 归还文件大小
    if total_size:
        request.tarcer.project.user_space -= delete_obj.file_size
        request.tracer.project.save()

    delete_obj.delete()
    return JsonResponse({"status": True})


@csrf_exempt
def file_upload(request, project_id):
    """文件上传完成之后，从前端接受到文件信息，并写入数据库"""
    # 使用modelform进行校验
    form = FileModelForm(request, data=request.POST)
    if form.is_valid():
        pass

    # 根据key和etag再去桶中校验数据
    return JsonResponse({"data": "OK!"})


@csrf_exempt
def cos_credential(request, project_id):
    """获取cos上传时的临时凭证"""
    # 向前端返回临时凭证的时候，做容量限制：单文件&多文件

    # 获取要上传的每个文件&文件大小
    # 这里接受的是一个前端经JSON处理的data ==> json.loads()
    total_size = 0
    file_list = json.loads(request.body.decode('utf-8'))
    per_file_max = request.tracer.price_policy.per_file_size * 1024 * 1024
    # 首先校验当文件大小限制
    for item in file_list:
        if item["size"] > per_file_max:
            return JsonResponse({
                "status": False,
                "error": "当文件超出限制：{}， 最大{}M，".format(item["name"], request.tracer.price_policy.per_file_size),
                "a_info": "请升级会员！"
            })
        total_size += item["size"]

    # 单个文件没有超出限制的话，查看总容量
    more_max = request.tracer.price_policy.project_space * 1024 * 1024 * 1024  # 项目的允许空间
    use_now = request.tracer.project.user_space  # 项目已使用空间
    if use_now + total_size > more_max:
        return JsonResponse({"status": False, "error": "容量超出限制，请升级会员！", "src": "请升级会员！"})

    data = credential(request.tracer.project.bucket, request.tracer.project.region)
    return JsonResponse({"status": True, "data": data})
