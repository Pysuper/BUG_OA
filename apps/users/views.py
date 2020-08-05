from random import randrange
from django.shortcuts import render, HttpResponse

from utils.tencent.send_msg import send_sms_single


# Create your views here.
def send_sms(request):
    """发送短信"""
    code = randrange(100000, 999999)
    res = send_sms_single("18895358393", 682840, [code, ])
    if res["result"] == 0:
        return HttpResponse('OK')
    else:
        return HttpResponse(res["errmsg"])
