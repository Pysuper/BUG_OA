from .models import Wiki
from django.urls import reverse
from django.http import JsonResponse
from .wiki_forms import WikiModelForm
from django.views.generic.base import View
from django.shortcuts import render, redirect
from rest_framework.viewsets import ViewSet, ModelViewSet


# Create your views here.

#
# class ParseWiki(ModelViewSet):
#     """使用类视图处理wiki的CUPD"""
#
#     ...
#

def wiki(request, project_id):
    """
    这里访问wiki首页的同时，处理详情页的信息
    :param request:
    :param project_id:
    :return:
    """
    wiki_id = request.GET.get("wiki_id")
    if wiki_id and wiki_id.isdecimal():  # 判断当前的数据是不是数字
        wiki_obj = Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
        return render(request, 'manages/wiki/wiki.html', {"wiki_obj": wiki_obj})
    return render(request, 'manages/wiki/wiki.html')


def delete_wiki(request, project_id, wiki_id):
    """删除wiki"""
    Wiki.objects.filter(id=wiki_id, project_id=project_id).delete()
    url = reverse('manages:wiki:home', kwargs={"project_id": project_id})
    return redirect(url)


def edit_wiki(request, project_id, wiki_id):
    """编辑"""
    wiki_obj = Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_obj:
        url = reverse('manages:wiki:home', kwargs={"project_id": project_id})
        return redirect(url)

    if request.method == "GET":
        form = WikiModelForm(request, instance=wiki_obj)
        return render(request, 'manages/wiki/wiki_form.html', {"form": form})
    form = WikiModelForm(request, data=request.POST, instance=wiki_obj)

    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1

        form.instance.project = request.tracer.project
        form.save()
        url = reverse('manages:wiki:home', kwargs={"project_id": project_id})
        preview_url = "{0}?wiki_id={1}".format(url, wiki_id)
        return redirect(preview_url)
    return render(request, "manages/wiki/wiki_form.html", {"form": form})


class AddWiki(View):
    def get(self, request, project_id):
        form = WikiModelForm(request, )
        return render(request, 'manages/wiki/wiki_form.html', {"form": form})

    def post(self, request, project_id):
        form = WikiModelForm(request, data=request.POST)
        if form.is_valid():
            # 添加数据之前，添加一次 对深度 的判断：是否已选择父文章
            if form.instance.parent:
                form.instance.depth = form.instance.parent.depth + 1
            else:
                form.instance.depth = 1

            form.instance.project = request.tracer.project
            form.save()
            url = reverse('manages:wiki:home', kwargs={"project_id": project_id})
            return redirect(url)
        return render(request, 'manages/wiki/wiki_form.html', {"error": form.errors})


def catalog(request, project_id):
    # 只显示当前项目的目录
    # data = Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title', 'parent_id')
    # data = Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id')
    data = Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by("depth", "id")
    return JsonResponse({"status": True, "data": list(data)})
