"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic.base import TemplateView, RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),  # index页面
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),  # favicon图标

    url(r'^user/', include(('users.urls', "user"), namespace="user")),  # 使用namespace， 防止多个app时前缀重名
    url(r'^project/', include(('project.urls', "project"), namespace="project")),
    url(r'^manage/(?P<project_id>\d+)/', include(('manages.urls', "manages"), namespace="manages")),
]
