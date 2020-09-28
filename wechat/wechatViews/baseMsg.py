import time
class Msg(object):
    def __init__(self, xmlData):
        # 返回的 ToUserName 和 FromUserName要相反哦！！
        self.ToUserName = xmlData.find('FromUserName').text
        self.FromUserName = xmlData.find('ToUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text

        self.MsgId = None
        self.Content = None
        self.PicUrl = None
        self.MediaId = None
        self.Event = None
        self.EventKey = None

        self.ReturnDict = dict()
        self.ReturnDict['ToUserName'] = self.ToUserName
        self.ReturnDict['FromUserName'] = self.FromUserName
        self.ReturnDict['MsgType'] = self.MsgType
        self.ReturnDict['CreateTime'] = int(time.time())
        # print(f'fromUserNAme:{self.ToUserName}')

    def send_text(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.ReturnDict)