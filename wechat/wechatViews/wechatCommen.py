import hashlib
import json
from django.utils.encoding import smart_str
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import time
import requests
import traceback

from wechat.wechatViews.textMsg import TextMsg

class WechatMsg:
    @classmethod
    def runCommen(cls, request, _token):
        if request.method == 'GET':
            print("验证微信身份")
            # 接收微信服务器get请求发过来的参数
            signature = request.GET.get('signature', None)
            timestamp = request.GET.get('timestamp', None)
            nonce = request.GET.get('nonce', None)
            echostr = request.GET.get('echostr', None)
            
            # 服务器配置中的token
            token = _token
            
            # 把参数放到list中排序后合成一个字符串，
            # 再用hash1加密得到新的字符串与微信发来的signature对比，
            # 如果相同就返回echostr给服务器， 校验通过
            hashlist = [token, timestamp, nonce]
            hashlist.sort()
            hashstr = ''.join([str(s) for s in hashlist])
            hashstr = hashlib.sha1(hashstr.encode("utf-8")).hexdigest()

            if hashstr == signature:
                return HttpResponse(echostr)
            else:
                return HttpResponse('Verify Failed')

        else:
            othercontent = cls.autoreply(request)
            return HttpResponse(othercontent)
            
    @classmethod
    def autoreply(cls, request):
        '''
        微信服务器推送消息是xml的，
        根据ElementTree来解析出的不同xml内容返回不同的回复信息，
        '''
        try:
            webData = request.body
            xmlData = ET.fromstring(webData)
            MsgType = xmlData.find('MsgType').text
            try:
                if MsgType == 'text':
                    replyMsg = TextMsg(xmlData)
                    return replyMsg.send_text()
                elif MsgType == 'image':
                    replyMsg = TextMsg(xmlData)     
                    return replyMsg.send_text()
                elif MsgType == 'voice':
                    replyMsg = TextMsg(xmlData)     
                    return replyMsg.send_text()
                elif MsgType == 'video':           
                    return replyMsg.send_text()
                elif MsgType == 'shortvideo':
                    return replyMsg.send_text()
                elif MsgType == 'location':          
                    return replyMsg.send_text()
                else:
                    MsgType == 'link'
                    return replyMsg.send_text()
            except:
                print(traceback.format_exc())
        except Exception as e:
            return e

if __name__ == "__main__":
    pass
