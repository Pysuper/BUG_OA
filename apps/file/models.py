from django.db import models
from project.models import Project
from users.models import UserInfo


# Create your models here.
class FileRepository(models.Model):
    """文件管理"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    file_type_choices = ({1, "文件"}, {2, "文件夹"},)
    file_type = models.SmallIntegerField(choices=file_type_choices, verbose_name="类型")
    name = models.CharField(max_length=32, help_text="文件、文件名", verbose_name="文件夹名称")
    key = models.CharField(max_length=128, null=True, blank=True, verbose_name="COS_KEY")
    file_size = models.IntegerField(null=True, blank=True, verbose_name="文件大小")
    file_path = models.CharField(max_length=255, null=True, blank=True, verbose_name="文件路径")
    parent = models.ForeignKey('self', null=True, blank=True, related_name="child", on_delete=models.CASCADE, verbose_name="父级目录")
    update_user = models.ForeignKey(UserInfo, null=True, on_delete=models.SET_NULL, verbose_name="最新更新者")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
