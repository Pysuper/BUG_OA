from django.db import models
from setting.develop import COLOR_CHOICES


# Create your models here.
class Project(models.Model):
    """项目"""
    name = models.CharField(verbose_name="项目名称", max_length=32)
    color = models.CharField(verbose_name="颜色", choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name="项目描述", max_length=25, null=True, blank=True)
    user_space = models.IntegerField(verbose_name="项目已使用空间", default=0)
    star = models.BooleanField(verbose_name="星标", default=0)

    bucket = models.CharField(verbose_name="腾讯对象存储桶", max_length=128)
    region = models.CharField(verbose_name="腾讯对象存储区域", max_length=32)

    join_count = models.SmallIntegerField(verbose_name="参与人数", default=1)
    creator = models.ForeignKey(verbose_name="创建者", to="UserInfo")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class ProjectUser(models.Model):
    """项目参与者"""
    user = models.ForeignKey(verbose_name="项目参与者", to="UserInfo")
    project = models.ForeignKey(verbose_name="项目名称", to="Project")

    star = models.BooleanField(verbose_name="星标", default=False)

    create_time = models.DateTimeField(verbose_name="加入时间", auto_now_add=True)
