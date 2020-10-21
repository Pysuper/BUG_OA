from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def dashboard(request, project_id):
    return render(request, 'manages/dashboard/dashboard.html')


def issues(request, project_id):
    return render(request, 'manages/issues/issues.html')


def statistics(request, project_id):
    return render(request, 'manages/statistics/statistics.html')


def setting(request, project_id):
    return render(request, 'manages/instal/setting.html')
