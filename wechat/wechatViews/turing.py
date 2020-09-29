#coding=utf-8

import json
import requests
import traceback
from doomfist.log import log

api_url = "http://openapi.tuling123.com/openapi/api/v2"
json_path = r'wechat\wechatViews\turing.json'

class TuringDome(object):
    def __init__(self,json_path="",api_url=""):
        self.json_path = json_path
        self.api_url = api_url
        # self.text_input = input('请输入我的问话\n我：')

    def readJson(self):
        '''获取json文件'''
        with open(self.json_path,'r',encoding='utf-8') as f_json:
            json_data = json.load(f_json)
        return json_data

    def textInput(self):
        '''用变量text_input替换text的value值'''
        req = self.readJson()
        req['perception']['inputText']['text'] = self.text_input
        req['userInfo']['userId'] = self.userId
        return req

    def dumpsJson(self):
        '''将json字符串转化成dict格式'''
        req = self.textInput()
        req = json.dumps(req, sort_keys = True, indent = 4,).encode('utf8')
        return req

    def urllibRequestResponse(self):
        req = self.dumpsJson()
        res = requests.post(self.api_url, data = req, headers = {'content-type': 'application/json'})
        response_str = eval(res.text)
        return response_str

    def getTuringResponse(self, text_input, userId):
        '''取得机器人返回的语句并输出'''
        try:
            self.text_input, self.userId = text_input, userId
            response_dict = self.urllibRequestResponse()
            try:
                results_text = response_dict.get('results')[0]['values']['text']
            except:
                results_text = response_dict.get('results')[-1]['values']['text'] + response_dict.get('results')[0]['values']['url']
        except Exception as e:
            log.error(f'图灵机器人报错：{e}')
            log.error(traceback.format_exc())
            return '小茗出错了哦，请稍后再跟小茗聊天吧~'
        return results_text

    def talkToTheTuring(self):
        while True:
            if self.text_input != "exit:":
                self.getTuringResponse(self.text_input, '1')
                self.text_input = input('请输入我的问话\n我：')
            else:
                log.info("*****结束对话！*****")
                break

turingDome = TuringDome(json_path = json_path, api_url = api_url)

if __name__ == '__main__':
    td = TuringDome(json_path = json_path, api_url = api_url)
    td.talkToTheTuring()
    # td.getTuringResponse()
