from django.http import JsonResponse

from .models import Wiki
from django.urls import reverse
from .wiki_forms import WikiModelForm
from django.views.generic.base import View
from django.shortcuts import render, redirect


# Create your views here.
def wiki(request, project_id):
    return render(request, 'manages/wiki/wiki.html')


class AddWiki(View):
    def get(self, request, project_id):
        form = WikiModelForm(request, )
        return render(request, 'manages/wiki/add.html', {"form": form})

    def post(self, request, project_id):
        form = WikiModelForm(request, data=request.POST)
        if form.is_valid():
            form.instance.project = request.tracer.project
            form.save()
            url = reverse('manages:wiki:home', kwargs={"project_id": project_id})
            return redirect(url)
        return render(request, 'manages/wiki/add.html', {"error": form.errors})


def catalog(request, project_id):
    # 只显示当前项目的目录
    # data = Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title', 'parent_id')
    data = Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id')
    return JsonResponse({"status": True, "data": list(data)})
