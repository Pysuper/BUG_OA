from django.db import models

# Create your models here.
from project.models import Project


class Wiki(models.Model):
    project = models.ForeignKey(Project, verbose_name="项目", on_delete=models.CASCADE)
    title = models.CharField(max_length=32, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    depth = models.IntegerField(default=1, verbose_name="深度")   # 新添加数据的时候，添加一个default
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children", on_delete=models.CASCADE, verbose_name="父文章")

    def __str__(self):
        return self.title