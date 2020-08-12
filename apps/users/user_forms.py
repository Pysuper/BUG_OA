# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : user_forms
# Datetime : 2020/8/11 上午10:13


from django import forms
from utils import encrypt
from random import randrange
from .models import UserInfo
from setting.variable import *
from utils.bootstrap import BootStrapForm
from django_redis import get_redis_connection
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from utils.tencent.send_msg import send_sms_single


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    """
    ModelForm组件，一个一个校验
    """
    password = forms.CharField(
        label="密码",
        min_length=8,
        max_length=64,
        error_messages={
            "min_length": "密码长度不能小于8个字符",
            "max_length": "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput
    )
    password_2 = forms.CharField(
        label="重复密码",
        min_length=8,
        max_length=64,
        error_messages={
            "min_length": "重复密码长度不能小于8个字符",
            "max_length": "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput)
    phone = forms.CharField(label="手机号码", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误')])
    code = forms.CharField(label="验证码", widget=forms.TextInput())

    class Meta:
        model = UserInfo
        # fields = "__all__"
        fields = ['username', 'email', 'password', 'password_2', 'phone', 'code']  # 之低昂返回的顺序

    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = UserInfo.objects.filter(username=username).exists()
        if exists:
            return ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        exists = UserInfo.objects.filter(email=email).exists()
        if exists:
            return ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        """在这里对密码进行加密"""
        password = self.cleaned_data["password"]
        return encrypt.md5(password)

    def clean_password_2(self):
        """cleaned_data: 已校验的字段"""
        password = self.cleaned_data["password"]
        password2 = encrypt.md5(self.cleaned_data["password_2"])
        if password != password2:
            raise ValidationError("两次密码不一致")
        return password2

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        exists = UserInfo.objects.filter(phone=phone).exists()
        if exists:
            raise ValidationError("当前手机已注册")
        return phone

    def clean_code(self):
        """校验验证码的时候，取出之后就把redis中的数据删除"""
        code = self.cleaned_data["code"]
        # phone = self.data["phone"]

        # 异常的处理
        phone = self.cleaned_data.get("phone")
        if not phone:
            return code

        conn = get_redis_connection()

        redis_code = conn.get(phone)
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")

        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError("验证码错误，请重新输入")

        # TODO： 当我们获取数据， 校验完成之后，删除redis中的数据
        # conn.delete(phone)

        return code


class SendSmsForm(forms.Form):
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

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

        if req_type == "login":
            if not exists:
                raise ValidationError("手机号不存在")
        else:
            if exists:
                raise ValidationError("手机号已存在")

        # 发送短信
        code = randrange(100000, 999999)
        sms_info = send_sms_single(phone, req_type, [code, ])
        if sms_info["result"] != 0:
            raise ValidationError("短信发送失败，{}".format(sms_info["errmsg"]))

        # 写入redis
        conn = get_redis_connection()
        conn.set(phone, code, ex=60)
        print(code)
        return phone


class LoginSmsForm(BootStrapForm, forms.Form):
    phone = forms.CharField(label="手机号码", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误')])
    code = forms.CharField(label="验证码", widget=forms.TextInput())

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        # exists = UserInfo.objects.filter(phone=phone).exists()    # 返回的是一个字符串
        user_obj = UserInfo.objects.filter(phone=phone).first()  # 返回的是一个对象
        if not user_obj:
            raise ValidationError("当前手机号码不存在")
        return user_obj

    def clean_code(self):
        """
        获取验证码的时候，zhijie
        :return:
        """
        code = self.cleaned_data["code"]
        user_obj = self.cleaned_data.get("phone")

        # 手机号码不存在，则验证码无需校验
        if not user_obj.phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(user_obj.phone)
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError("验证码错误，请重新输入")
        return code


class LoginUserForm(BootStrapForm, forms.Form):
    username = forms.CharField(label="用户名 / 手机号 / 邮箱")
    password = forms.CharField(
        label="密码",
        min_length=8,
        max_length=64,
        error_messages={
            "min_length": "密码长度不能小于8个字符",
            "max_length": "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput(render_value=True),
    )
    img_code = forms.CharField(label="图片验证码", widget=forms.TextInput())

    def __init__(self, request, *args, **kwargs):
        """Form中没有request ==> 设置request ==> 调用的时候传入"""
        super().__init__(*args, **kwargs)
        self.request = request

    """这里不写===> 不能使用pass
    def clean_username(self):
        # 在view.py中编写, 后续可以直接返回
        pass
    """

    def clean_password(self):
        """在这里对密码进行加密"""
        password = self.cleaned_data["password"]
        return encrypt.md5(password)

    def clean_img_code(self):
        """校验用户输入的图片验证码是否正确"""
        code = self.cleaned_data["img_code"]  # 读取用户输入的code
        session_code = self.request.session.get("image_code")  # 从session中获取code
        if not session_code:
            raise ValidationError("验证码已过期， 请重新获取！")

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError("验证码输入错误， 请重新输入！")

        return code
