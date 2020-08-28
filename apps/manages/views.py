from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def dashboard(request, project_id):
    return render(request, 'manages/dashboard.html')


def issues(request, project_id):
    return render(request, 'manages/issues.html')


def statistics(request, project_id):
    return render(request, 'manages/statistics.html')


def file(request, project_id):
    return render(request, 'manages/file.html')


def wiki(request, project_id):
    return render(request, 'manages/wiki.html')


def setting(request, project_id):
    return render(request, 'manages/setting.html')
