from wechat.wechatViews.baseMsg import Msg
from wechat.wechatViews.turing import turingDome

class VoiceMsg(Msg):
    def __init__(self, xmlData):
        super().__init__(xmlData)
        self.get_msg(xmlData)
        self.do_func()

    def get_msg(self, xmlData):
        self.Recognition = xmlData.find('Recognition').text
    
    def do_func(self):
        # 语音无消息
        if not self.Recognition:
            self.ReturnDict['Content'] = '不知道你在说什么噢'

        # 机器人回答
        else:
            # UserName固定字符当图灵userid
            self.ReturnDict['Content'] = turingDome.getTuringResponse(self.Content, self.ToUserName[7:].replace("_", ""))