from wechat.wechatViews.baseMsg import Msg
from wechat.wechatViews.rainbow import ShaDiao
from wechat.models import PersonalImg
import random

class EventMsg(Msg):

    def __init__(self, xmlData):
        
        self.sendImg = False
        super().__init__(xmlData)
        self.get_msg(xmlData)
        self.do_func()

    def get_msg(self, xmlData):
        try:
            self.EventKey = xmlData.find('EventKey').text
        except:
            try:
                self.Event = xmlData.find('Event').text
            except:
                pass

    def do_func(self):
        '''
        根据用户点击的事件的key字段来判断回复什么
        '''
        if self.EventKey == 'HELP':
            content = "关键字：\n" + \
                "“快递123456”查询快递情况\n" + \
                "“笔记XXX”记录笔记\n" + \
                "“获取笔记”获取所有笔记"
            self.ReturnDict['Content'] = content

        elif self.EventKey == 'RAINBOW':
            self.ReturnDict['Content'] = ShaDiao.get_one_p()
        
        elif self.EventKey == 'SELFPIC':
            count = PersonalImg.objects.filter(userid = self.ToUserName).count()
            if count == 0:
                self.ReturnDict['Content'] = '给我发一张你的照片吧，也可以多发几张噢'
            else:
                imgs = PersonalImg.objects.filter(userid = self.ToUserName)
                count = 0
                img = random.choice(imgs)
                self.ReturnDict['PicUrl'] = img.PicUrl
                self.ReturnDict['MediaId'] = img.MediaId
                self.sendImg = True

        elif self.Event == 'subscribe':
            self.ReturnDict['Content'] = ShaDiao.get_one_p()
        
                    
    def send_img(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.ReturnDict)