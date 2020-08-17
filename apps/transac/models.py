from django.db import models
from users.models import UserInfo


# Create your models here.
class PricePolicy(models.Model):
    """收费类型"""
    category_choices = ((1, "免费版"), (2, "收费版"), (3, "其他",))

    # SmallIntegerField 小范围
    category = models.SmallIntegerField(verbose_name="收费类型", choices=category_choices, default=1)

    title = models.CharField(verbose_name="标题", max_length=32)
    # PositiveIntegerField 正整数类型
    price = models.PositiveIntegerField(verbose_name="价格")

    project_num = models.PositiveIntegerField(verbose_name="项目数")
    project_member = models.PositiveIntegerField(verbose_name="项目成员数")
    project_space = models.PositiveIntegerField(verbose_name="单项目空间")
    per_file_size = models.PositiveIntegerField(verbose_name="单文件大小")

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class Transaction(models.Model):
    """交易记录"""
    status_choice = ((1, "已支付"), (2, "未支付",))
    status = models.SmallIntegerField(verbose_name="支付状态", choices=status_choice)

    order = models.CharField(verbose_name="订单号", max_length=64, unique=True)  # unique唯一索引
    user = models.ForeignKey(UserInfo, verbose_name="用户", on_delete=models.CASCADE)
    pro_policy = models.ForeignKey(PricePolicy, verbose_name="价格策略", on_delete=models.SET_NULL, null=True, blank=True)

    count = models.IntegerField(verbose_name="数量(年)", help_text="0表示无限期")

    price = models.IntegerField(verbose_name="实际支付价格")

    start_datetime = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)

    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
