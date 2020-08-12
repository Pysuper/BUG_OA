from django.shortcuts import render
from django.http import JsonResponse
from .user_forms import RegisterModelForm, SendSmsForm, LoginSmsForm
from django.views.generic.base import View


# Create your views here.


class Register(View):
    """用户注册，使用forms中的钩子进行校验"""

    def get(self, request):
        form = RegisterModelForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            form.save()  # 写入数据库==>instance
            return JsonResponse({"status": True, "data": "/user/login/sms/"})
        return JsonResponse({"status": False, "error": form.errors})


class LoginSms(View):
    """短信登录"""

    def get(self, request):
        form = LoginSmsForm()
        return render(request, 'login_sms.html', {"form": form})

    def post(self, request):
        form = LoginSmsForm(data=request.POST)  # 使用Form校验的时候，要将request的参数发送到Form中
        if form.is_valid():
            user_obj = form.cleaned_data["phone"]  # 这里获取的就是user的对象==>写入session
            print(user_obj.username)

            # request.session["user_id"] = user_obj.id
            # request.session["user_name"] = user_obj.username
            return JsonResponse({"status": True, "data": "/"})
        return JsonResponse({"status": False, "error": form.errors})


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号：不能为空, 格式是否正确
    if form.is_valid():
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
