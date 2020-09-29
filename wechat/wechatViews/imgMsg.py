from wechat.wechatViews.baseMsg import Msg
from wechat.models import PersonalImg
from django.conf import settings
import requests
import json

class ImgMsg(Msg):

    def __init__(self, xmlData):
        super().__init__(xmlData)
        self.get_msg(xmlData)
        self.do_func()

    def get_msg(self, xmlData):
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text
        self.ReturnDict['PicUrl'] = self.PicUrl
        self.ReturnDict['MediaId'] = self.MediaId

    def do_func(self):
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={settings.ACCESS_TOKEN}&type=image"
        res = requests.get(self.PicUrl)
        with open('demo.jpg', 'wb') as f:
            f.write(res.content)
        file = {'media': open('demo.jpg', 'rb')}

        r = requests.post(url, files = file)
        parse_json = json.loads(r.content.decode())
        if parse_json.get('media_id', ''):
            count = PersonalImg.objects.filter(userid = self.ToUserName).count()
            if count >= 7:
                PersonalImg.objects.filter(userid = self.ToUserName).exclude(adminSet = True).order_by('-pk')[0].delete()
            PersonalImg.objects.get_or_create(userid = self.ToUserName, MediaId = parse_json['media_id'], PicUrl = self.PicUrl)
            self.ReturnDict['Content'] = '收到了噢~'
        else:
            self.ReturnDict['Content'] = '上传失败ORZ'
        
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

        