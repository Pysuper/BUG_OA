from django.shortcuts import render


# Create your views here.
def matter(request, project_id):
    return render(request, 'manages/issues/issues.html')
