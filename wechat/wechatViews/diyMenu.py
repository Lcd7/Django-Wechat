import requests
import json
import sys

appID = 'wxd1b5b8e835a07348'      
appsecret = '19aef1ef92b95619bae56839e242f94f'   

menu = {                      
    "button":[
    {
        "type": "click",       
        "name": "呜呼~!",
        "key": 'RAINBOW',
    },
    {
        "name": "在吗？",
        "sub_button": [
            {
                "type": "view",
                "name": "Tech-Log",
                "url": "http://www.ruanyifeng.com/blog/"
            },
            {
                "type": "view",
                "name": "FreeMP3",
                "url": "http://tool.liumingye.cn/music/?page=homePage"
            },
            {
                "type": "view",
                "name": "HDFilm",
                "url": "http://pianyuan.la/"
            }
        ]
    },
    {
        "name": "上勾拳!",
        "sub_button": [
            {
                "type": "click",
                "name": "开心OVO",
                "key": "SELFPIC"
            },
            {
                "type": "click",
                "name": "关键字",
                "key": "HELP"
            }
        ]
    }
    ]
}

def getMenuRequest():
    gettoken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appID + '&secret=' + appsecret
    res = requests.get(gettoken)
    res = eval(res.text)
    access_token = res['access_token']
    posturl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=" + access_token

    req = requests.get(posturl)
    print(req.text)

def createMenuRequest(menu):
    data = json.dumps(menu, ensure_ascii=False).encode('utf-8')
    gettoken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appID + '&secret=' + appsecret
    res = requests.get(gettoken)
    res = res.json()
    access_token = res['access_token']
    postcreateurl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token

    req = requests.post(postcreateurl, data = data)
    # result = json.loads(req)   
    print(req.text)  
    # if result["errcode"] == 0:
    #     tkMessageBox.showinfo('成功！',"errmsg:"+str(result["errmsg"]))
    # else:
    #     tkMessageBox.showinfo('失败！', "errcode:"+str(result["errcode"])+"\n"+"errmsg:" + str(result["errmsg"]))

if __name__ == "__main__":
    createMenuRequest(menu)
    # getMenuRequest()