import requests
import time
from django.conf import settings

def get_access_token():
    # global settings.ACCESS_TOEKN  
    while True:
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={settings.WXAPPID}&secret={settings.WXAPPSECRET}"
        res = requests.get(url)
        res = eval(res.text)
        settings.ACCESS_TOKEN = res.get('access_token', '')
        time.sleep(60 * 110)