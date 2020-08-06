from django import forms
from random import randrange
from .models import UserInfo
from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse
from django.core.exceptions import ValidationError
from utils.tencent.send_msg import send_sms_single


# Create your views here.
def send_sms(request):
    """发送短信"""
    code = randrange(100000, 999999)
    # res = send_sms_single("18895358393", 682840, [code, ])
    # res = send_sms_single("18879519910", 682840, [code, ])    # 刘
    res = send_sms_single("18879519910", 682840, [code, ])  # 鸡
    if res["result"] == 0:
        return HttpResponse('OK')
    else:
        return HttpResponse(res["errmsg"])


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


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {"form": form})


def index(request):
    # 去连接池中获取一个连接
    conn = get_redis_connection("default")
    conn.set('nickname', "zhengxingtao", ex=10)
    value = conn.get('nickname')
    print(value)
    return HttpResponse("OK")
