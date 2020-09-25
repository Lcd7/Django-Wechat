import time
class Msg(object):
    def __init__(self, xmlData):
        # 返回的 ToUserName 和 FromUserName要相反哦！！
        self.ToUserName = xmlData.find('FromUserName').text
        self.FromUserName = xmlData.find('ToUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

        self.Content = None
        self.PicUrl = None
        self.MediaId = None

        self.ReturnDict = dict()
        self.ReturnDict['ToUserName'] = self.ToUserName
        self.ReturnDict['FromUserName'] = self.FromUserName
        self.ReturnDict['MsgId'] = self.MsgId
        self.ReturnDict['MsgType'] = self.MsgType
        self.ReturnDict['CreateTime'] = int(time.time())
        # print(f'fromUserNAme:{self.ToUserName}')