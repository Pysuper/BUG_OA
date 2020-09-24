from django.shortcuts import render


# Create your views here.

def board(request, project_id):
    return render(request, 'manages/dashboard/dashboard.html')
