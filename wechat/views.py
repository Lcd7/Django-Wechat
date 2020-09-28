from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
import os
env_dist = os.environ

from wechat.wechatViews.wechatCommen import WechatMsg
from django.conf import settings
# import wechat.wechatViews

# Create your views here.

token = settings.WXTOKEN
appid = settings.WXAPPID
appsecret = settings.WXAPPSECRET

@csrf_exempt
def withCommen(request):
    return WechatMsg.runCommen(request, token)