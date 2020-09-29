import time
import datetime
import requests
import traceback
import random

from django.conf import settings
from doomfist.log import log
from wechat.wechatViews.baseMsg import Msg
from wechat.wechatViews.turing import turingDome
from wechat.models import PersonalLog
from wechat.wechatViews.rainbow import ShaDiao
from wechat.models import PersonalImg

# self.ToUserName[7:].replace("_", "") = 'cQ8bDxSfyUxbAj43HQm4':

class TextMsg(Msg):
    def __init__(self, xmlData):
        self.sendImg = False
        super().__init__(xmlData)
        self.get_msg(xmlData)
        self.do_func()

    def do_func(self):
        '''
        对用户发送的图/文信息进行分类回复
        '''
        # 表情包
        if self.Content == '【收到不支持的消息类型，暂无法显示】':
            self.ReturnDict['Content'] = '表情包我还看不懂噢'
        elif self.Content == '关键字':
            content = "关键字：\n" + \
                "“快递123456”查询快递情况\n" + \
                "“笔记XXX”记录笔记\n" + \
                "“获取笔记”获取所有笔记\n" + \
                "“电影”给你网址自己去找噢\n" + \
                "“音乐”可以搜歌可以解码vip歌\n" + \
                "“屁”获得精美彩虹屁一个\n" + \
                "“照片”随机给你最近一张照片\n" + \
                "“杂志”阮一峰科技日志\n"
            self.ReturnDict['Content'] = content

        # 关键字功能
        # 记录个人日志
        elif self.Content[:2] == '笔记':
            self.make_note()
        # 获取个人日志
        elif self.Content == '获取笔记':
            self.take_note()
        # 快递
        elif self.Content[:2] == '快递':
            self.check_express()
        # 电影
        elif self.Content == '电影':
            self.ReturnDict['Content'] = "http://pianyuan.la/\n这里电影电视剧资源还是挺全的，自己去找吧"
        # 音乐
        elif self.Content == '音乐':
            self.ReturnDict['Content'] = "http://tool.liumingye.cn/music/?page=homePage\n这里可以搜全网大部分的音乐，还可以把下载的vip歌曲解码噢"
        # 阮一峰杂志
        elif self.Content == '杂志':
            self.ReturnDict['Content'] = 'http://www.ruanyifeng.com/blog/\n周五划水必备'
        # 屁
        elif self.Content == '屁':
            self.ReturnDict['Content'] = ShaDiao.get_one_p()
        # 照片
        elif self.Content == '照片':
            self.pictures()

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
                log.info(traceback.format_exc())
                self.ReturnDict['Content'] = '好像记录失败咯，先回复“查询日志”来查询一下吧。'
            else:
                self.ReturnDict['Content'] = '记录成功咯'

    def take_note(self):
        content_list = []
        try:
            notes = PersonalLog.objects.filter(userid = self.ToUserName).order_by('pk')
            if not notes:
                self.ReturnDict['Content'] = '你还没有笔记噢'
            else:
                for note in notes:
                    content_list.append(str(note.pub_date)[:-13] + "\n" + note.content)
                self.ReturnDict['Content'] = '\n'.join(content_list)
        except:
            log.info(traceback.format_exc())

    def pictures(self):
        imgs = PersonalImg.objects.filter(userid = self.ToUserName)
        count = imgs.count()
        if count == 0:
            self.ReturnDict['Content'] = '给我发一张照片吧，也可以多发几张噢'
        else:
            img = random.choice(imgs)
            self.ReturnDict['PicUrl'] = img.PicUrl
            self.ReturnDict['MediaId'] = img.MediaId
            self.sendImg = True

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