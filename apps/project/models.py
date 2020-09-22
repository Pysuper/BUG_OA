from django.db import models
from users.models import UserInfo
from setting.develop import COLOR_CHOICES


# Create your models here.
class Project(models.Model):
    """项目"""
    name = models.CharField(verbose_name="项目名称", max_length=32)
    color = models.SmallIntegerField(verbose_name="颜色", choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name="项目描述", max_length=25, null=True, blank=True)
    user_space = models.IntegerField(verbose_name="项目已使用空间", default=0)
    star = models.BooleanField(verbose_name="星标", default=0)

    # 为每一个项目在COS中创建一个桶
    bucket = models.CharField(verbose_name="腾讯对象存储桶", max_length=128)
    region = models.CharField(verbose_name="腾讯对象存储区域", max_length=32)

    join_count = models.SmallIntegerField(verbose_name="参与人数", default=1)
    creator = models.ForeignKey(UserInfo, verbose_name="创建者", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    # 如果多对多的时候
    # 好处不大----查询的时候可以直接查询， 增加、删除、修改 都无法完成
    # 第三张关联表里面只有两个表的id==> 可以使用ManyToManyField
    # 第三张表中不止两个id的时候，可以使用through指定关联哪张表，同时使用through_fields指定管理的是哪些字段（这时候不会主动创建第三张表）
    # 使用through_fields, 对字段的顺序有要求，project-user， 另一张表里也要遵循这个顺序
    # project_user = models.ManyToManyField(to="UserInfo", through="ProjectUser", through_fields=("project", "user))


class ProjectUser(models.Model):
    """项目参与者"""
    user = models.ForeignKey(UserInfo, verbose_name="项目参与者", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, verbose_name="项目名称", on_delete=models.CASCADE)

    star = models.BooleanField(verbose_name="星标", default=False)

    create_time = models.DateTimeField(verbose_name="加入时间", auto_now_add=True)
