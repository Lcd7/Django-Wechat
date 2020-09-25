import time
import requests

from wechat.wechatViews.baseMsg import Msg
from wechat.wechatViews.turing import turingDome

class TextMsg(Msg):
    def __init__(self, xmlData):
        super().__init__(xmlData)
        self.get_msg(xmlData)

        # 图片
        if self.PicUrl:
            self.ReturnDict['Content'] = '已收到图片OVO'
        # 表情包
        elif self.Content == '【收到不支持的消息类型，暂无法显示】':
            self.ReturnDict['Content'] = '表情包我还看不懂噢'
        # 语音无消息
        elif not self.Content:
            self.ReturnDict['Content'] = '不知道你在说什么噢'
        # 快递
        elif self.Content[:2] == '快递':
            self.check_express()
        # 侮辱
        elif ('李陈冬' in self.Content or '七哥' in self.Content or '骑哥' in self.Content or '冬瓜皮' in self.Content \
            or '儿七' in self.Content or '李陈东' in self.Content)\
                and self.ToUserName[7:].replace("_", "") != 'cQ8bDxSfyUxbAj43HQm4': #我
            self.ReturnDict['Content'] = '七哥是你爹，艹Ta🐎内阁臭P'
        # 强哥
        elif '强哥' in self.Content or '杨强' in self.Content:
            self.ReturnDict['Content'] = '杨强老SP，强哥我敬你一杯'
        # 图灵
        else:
            # UserName固定字符当图灵userid
            self.ReturnDict['Content'] = turingDome.getTuringResponse(self.Content, self.ToUserName[7:].replace("_", ""))

    def get_msg(self, xmlData):
        try:
            self.Content = xmlData.find('Content').text
        except:
            try:
                self.Content = xmlData.find('Recognition').text
            except:
                self.PicUrl = xmlData.find('PicUrl').text
                self.MediaId = xmlData.find('MediaId').text
                self.ReturnDict['MediaId'] = self.MediaId
        self.ReturnDict['Content'] = self.Content

    def check_express(self):
        '''
        查快递
        '''
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                'Referer': 'https://www.kuaidi100.com/',
                'Host': 'www.kuaidi100.com',
            }
            expressNum = str(self.Content[2:])

            url_id = 'https://www.kuaidi100.com/autonumber/autoComNum'
            params_id = {
                'resultv2': '1',
                'text': self.Content[2:]
            }
            req_id = requests.post(url_id, params = params_id, headers = headers)
            result_id = req_id.json()
            comde = result_id['auto'][0]['comCode']
            res = requests.get(f'https://www.kuaidi100.com/query?type={comde}&postid={expressNum}&temp=0.8606797497352612&phone=', headers = headers)
            resDict = eval(res.text)
            if resDict.get('ischeck', 0):
                expMsg = f"{resDict.get('data')[0].get('ftime')}, 到达：{resDict.get('data')[0].get('context')}"
                self.ReturnDict['Content'] = expMsg
            else:
                self.ReturnDict['Content'] = resDict.get('message', '没有物流信息哦')
        except:
            self.ReturnDict['Content'] = resDict.get('message', '没有物流信息哦, 检查一下快递单号吧~')

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