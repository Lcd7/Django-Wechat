import time
import datetime
import requests
import traceback

from wechat.wechatViews.baseMsg import Msg
from wechat.wechatViews.turing import turingDome
from wechat.models import PersonalLog

# self.ToUserName[7:].replace("_", "") = 'cQ8bDxSfyUxbAj43HQm4': #我

class TextMsg(Msg):
    def __init__(self, xmlData):
        super().__init__(xmlData)
        self.get_msg(xmlData)
        self.do_func()

    def do_func(self):
        '''
        对用户发送的图/文信息进行分类回复
        '''
        # 图片
        if self.PicUrl:
            # print(f'PicUrl:{self.PicUrl}')
            self.ReturnDict['Content'] = '已收到图片OVO'
        # 表情包
        elif self.Content == '【收到不支持的消息类型，暂无法显示】':
            self.ReturnDict['Content'] = '表情包我还看不懂噢'

        # '''
        # 关键字功能
        # '''
        # 记录个人日志
        elif self.Content[:4] == '笔记':
            self.make_note()
            
        # 获取个人日志
        elif self.Content == '获取笔记':
            self.take_note()

        # 快递
        elif self.Content[:2] == '快递':
            self.check_express()

        # '''
        # 回复功能
        # '''
        # 语音无消息
        elif not self.Content:
            self.ReturnDict['Content'] = '不知道你在说什么噢'

        # 语音和文字都由机器人回答
        else:
            # UserName固定字符当图灵userid
            self.ReturnDict['Content'] = turingDome.getTuringResponse(self.Content, self.ToUserName[7:].replace("_", ""))

    def get_msg(self, xmlData):
        '''
        获取用户发来的文字和语音以及图片中的文字信息
        '''
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

    def make_note(self):
        if len(self.Content) == 4:
            self.ReturnDict['Content'] = '没有什么可记录的噢'
        else:
            pub_date = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
            try:
                PersonalLog.objects.create(userid = self.ToUserName, content = self.Content[4:], pub_date = pub_date)
            except:
                print(traceback.format_exc())
                self.ReturnDict['Content'] = '好像记录失败咯，先回复“查询日志”来查询一下吧。'
            else:
                self.ReturnDict['Content'] = '记录成功咯'

    def take_note(self):
        content_list = []
        try:
            notes = PersonalLog.objects.filter(userid = self.ToUserName).order_by('pk')
            for note in notes:
                content_list.append(str(note.pub_date)[:-13] + "\n" + note.content)
            self.ReturnDict['Content'] = '\n'.join(content_list)
        except:
            print(traceback.format_exc())
