from django.shortcuts import render


# Create your views here.
def count(request, project_id):
    return render(request, 'manages/statistics/statistics.html')
