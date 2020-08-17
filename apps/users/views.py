import uuid
from io import BytesIO
from .models import UserInfo
from datetime import datetime
from django.db.models import Q
from utils.image_code import check_code
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from transac.models import Transaction, PricePolicy
from .user_forms import RegisterModelForm, SendSmsForm, LoginSmsForm, LoginUserForm


# Create your views here.


class Register(View):
    """用户注册，使用forms中的钩子进行校验"""

    @staticmethod
    def get(request):
        form = RegisterModelForm()
        return render(request, 'register.html', {"form": form})

    @staticmethod
    def post(request):
        form = RegisterModelForm(data=request.POST)

        if form.is_valid():
            # 在这里添加用户交易记录
            instance = form.save()  # 写入数据库==>instance
            policy_obj = PricePolicy.objects.filter(category=1, title="个人免费版").first()

            Transaction.objects.create(
                status=2,
                order=str(uuid.uuid4()),
                user=instance,
                pro_policy=policy_obj,
                count=0,
                price=0,
                start_datetime=datetime.now(),
            )
            return JsonResponse({"status": True, "data": "/user/login/user/"})
        return JsonResponse({"status": False, "error": form.errors})


class LoginSms(View):
    """短信登录"""

    @staticmethod
    def get(request):
        form = LoginSmsForm()
        return render(request, 'login_sms.html', {"form": form})

    @staticmethod
    def post(request):
        form = LoginSmsForm(data=request.POST)  # 使用Form校验的时候，要将request的参数发送到Form中
        if form.is_valid():
            user_obj = form.cleaned_data["phone"]  # 这里获取的就是user的对象==>写入session

            # 登录成功
            request.session["user_id"] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 14)

            return JsonResponse({"status": True, "data": "/"})
        return JsonResponse({"status": False, "error": form.errors})


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号: 不能为空, 格式是否正确
    if form.is_valid():
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def image_code(request):
    """生成图片验证码"""
    image_obj, code = check_code()

    # 将code存入session，并设置60s的过期时间
    request.session["image_code"] = code
    request.session.set_expiry(60)

    # 把图片写入到内存中
    stream = BytesIO()
    image_obj.save(stream, 'png')
    return HttpResponse(stream.getvalue())


class LoginUser(View):
    @staticmethod
    def get(request):
        form = LoginUserForm(request)
        return render(request, 'login_user.html', {"form": form})

    @staticmethod
    def post(request):
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # 用户名
            # user_obj = UserInfo.objects.filter(username=username, password=password).first()

            # 用户名 / 手机号 / 邮箱 ==> 复杂查询--Q
            user_obj = UserInfo.objects.filter(
                Q(username=username) |
                Q(phone=username) |
                Q(email=username)).filter(
                password=password
            ).first()

            if user_obj:  # 登录成功
                request.session["user_id"] = user_obj.id
                request.session.set_expiry(60 * 60 * 24 * 14)
                return redirect('/')

            form.add_error("username", "用户名或密码错误！")  # 将错误信息添加到form中
        return render(request, 'login_user.html', {"form": form})


def logout(request):
    request.session.flush()
    return redirect('/')
