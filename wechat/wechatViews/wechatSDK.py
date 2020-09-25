from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest

from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
from wechat_sdk.context.framework.django import DatabaseContextStore
from wechat.models import KeyWord as KeyWordModel
# Create your views here.


def runSDK(request, wechat_instance):
    if request.method == 'GET':
        # 检验合法性
        # 从reques 中提取基本信息(signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
            signature = signature, timestamp = timestamp, nonce = nonce
        ):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type = "text/plain"
        )
    
    # POST 解析本次请求的XML
    try:
        wechat_instance.parse_data(data = request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
    # 利用本次请求中的用户OpenID来初始化上下文对话
    context = DatabaseContextStore(openid = message.source)

    response = None

    if isinstance(message, TextMessage):
        step = context.get('step', 1)   #当前对话次数
        # last_text = context.get('last_text)
        content = message.content.strip()   # 当前会话内容

        if message.content == '新闻':
            response = wechat_instance.response_news([
                {
                    'title': '致敬八二',
                    'description': '致敬巴萨主教练巴尔韦德',
                    'url': 'www.cctv5.com',
                },
                {
                    {
                    'title': '致敬林皇',
                    'description': '致敬曼联功勋球员林加德大帝',
                    'url': 'www.cctv5.com',
                }
                }
            ])
            return HttpResponse(response, content_type = "application/xml")
        
        else:
            try:
                keyword_object = KeyWordModel.objects.get(Keyword = content)
                reply_text = keyword_object.content
            except KeyWordModel.DoesNotExist:
                try:
                    keyword_object = KeyWordModel.objects.get(Keyword = content).content
                except KeyWordModel.DoesNotExist:
                    reply_text = ('/:P-(好委屈，数据库翻个遍也没找到你输的关键词！\n'
                        '试试下面这些关键词吧：\nKEYWORD_LIST\n'
                        '<a href="http://www.rxnfinder.org">RxnFinder</a>'
                        '感谢您的支持！/:rose')
    
        # 将新的数据存入上下文对话中
        context['step'] = step + 1
        context['last_text'] = content
        # 临时数据存入数据库 很重要
        context.save()

        if 'KEYWORD_LIST' in reply_text:
            keyword_object = KeyWordModel.objects.exclude(
                keyword__in = ['关注事件', '测试', 'test', '提示']
            ).filter(published = True)
            keywords = (f'{str(i)}{k.keyword}' for i, k in enumerate(keyword_object, 1))
            reply_text = reply_text.replace('KEYWORD_LIST', '\n'.join(keywords))

    elif isinstance(message, VoiceMessage):
        reply_text = '语音已收到,谢谢/:P-('
    elif isinstance(message, ImageMessage):
        reply_text = '图片已收到,谢谢/:P-('
    elif isinstance(message, VideoMessage):
        reply_text = '视频已收到,谢谢/:P-('
    elif isinstance(message, LinkMessage):
        reply_text = '链接已收到,谢谢/:P-('
    elif isinstance(message, LocationMessage):
        reply_text = '位置已收到,谢谢/:P-('
    elif isinstance(message, EventMessage):  # 事件信息
        if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            follow_event = KeyWordModel.objects.get(keyword='关注事件')
            reply_text = follow_event.content
 
            # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
            if message.key and message.ticket:
                reply_text += '\n来源：扫描二维码关注'
            else:
                reply_text += '\n来源：搜索名称关注'
        elif message.type == 'unsubscribe':
            reply_text = '取消关注事件'
        elif message.type == 'scan':
            reply_text = '已关注用户扫描二维码！'
        elif message.type == 'location':
            reply_text = '上报地理位置'
        elif message.type == 'click':
            reply_text = '自定义菜单点击'
        elif message.type == 'view':
            reply_text = '自定义菜单跳转链接'
        elif message.type == 'templatesendjobfinish':
            reply_text = '模板消息'
    
    response = wechat_instance.response_text(content = reply_text)
    return HttpResponse(response, content_type = "application/xml")