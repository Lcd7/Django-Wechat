from threading import Thread
from wechat.wechatViews.getAccessToken import get_access_token

daemonThread = Thread(target = get_access_token, )
daemonThread.daemon = True
daemonThread.start()