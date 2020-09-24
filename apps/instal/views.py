from django.shortcuts import render


# Create your views here.
def instal(request, project_id):
    return render(request, 'manages/instal/setting.html')
