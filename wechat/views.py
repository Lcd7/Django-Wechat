from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
import os
env_dist = os.environ

# from wechat.wechatViews.wechatSDK import runSDK
from wechat.wechatViews.wechatCommen import WechatMsg

# Create your views here.

token = env_dist.get('WXToken')
appid = env_dist.get('WXAppid')         # 机密
appsecret = env_dist.get('WXAppsecret') # 机密
wechat_instance = WechatBasic(
    token = token, 
    appid = appid,                  
    appsecret = appsecret  
)

# @csrf_exempt
# def withSDk(request):
#     return runSDK(request, wechat_instance)

@csrf_exempt
def withCommen(request):
    return WechatMsg.runCommen(request, token)