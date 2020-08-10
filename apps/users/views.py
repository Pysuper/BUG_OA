from django import forms
from random import randrange
from .models import UserInfo
from setting.variable import *
from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse
from django.core.exceptions import ValidationError
from utils.tencent.send_msg import send_sms_single


# Create your views here.
class RegisterModelForm(forms.ModelForm):
    phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^{1[3][4][5][6][7][8][9]}\d{9}$', '手机号码格式错误')])
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    password_2 = forms.CharField(label="重复密码", widget=forms.PasswordInput)
    code = forms.CharField(label="验证码", widget=forms.TextInput)

    class Meta:
        model = UserInfo
        # fields = "__all__"
        fields = ['username', 'email', 'password', 'password_2', 'phone', 'code']  # 之低昂返回的顺序

    def __init__(self, *args, **kwargs):
        """重写父类的初始化方法，添加html标签"""
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入{}".format(field.label)


class SendSmsForm(forms.Form):
    phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^{1[3][4][5][6][7][8][9]}\d{9}$', '手机号码格式错误')])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_phone(self):
        """手机校验的钩子"""
        phone = self.cleaned_data["phone"]

        # 判断短信模是否有问题
        req_type = self.request.GET.get("req_type")
        template_id = SMS_TEMPLATES.get(req_type)
        if not template_id:
            raise ValidationError("短信模板错误")

        # 校验数据库中是否已有手机号
        exists = UserInfo.objects.filter(phone=phone).exists()
        if exists:
            raise ValidationError("手机号已存在")

        return phone


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {"form": form})


def index(request):
    # 去连接池中获取一个连接
    conn = get_redis_connection("default")
    conn.set('nickname', "zheng xingtao", ex=10)
    value = conn.get('nickname')
    print(value)
    return HttpResponse("OK")


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)

    # 只是校验手机号：不能为空, 格式是否正确
    if form.is_valid():
        # 发短信
        # 写redis
        pass
    return HttpResponse("成功")
    # phone = request.GET.get("phone", None)
    # req_type = request.GET.get("req_type", None)
    # code = randrange(100000, 999999)
    # res = send_sms_single(phone, req_type, [code, ])
    # # res = send_sms_single("18879519910", 682840, [code, ])    # 刘
    # # res = send_sms_single("18879519910", 682840, [code, ])    # 鸡
    # if res["result"] == 0:
    #     return HttpResponse('OK')
    # else:
    #     return HttpResponse(res["errmsg"])
