import requests
import json
import random

class ShaDiao:
    
    wordDict = json.load(open(r"wechat\wechatViews\彩虹屁.json", "r", encoding = "utf-8")) 
    url = 'https://chp.shadiao.app/api.php'

    @classmethod
    def get_Ps(cls, num):
        for _ in range(num):
            res = requests.get(cls.url)
            html_text = res.text
            if html_text not in cls.wordDict:
                cls.wordDict[html_text] = ""
        json.dump(cls.wordDict, open(r"wechat\wechatViews\彩虹屁.json", "w", encoding = "utf-8"), ensure_ascii = False)

    @classmethod
    def get_one_p(cls):
        randNum = random.randint(0, len(cls.wordDict))
        # print(list(cls.wordDict.keys())[randNum])
        return list(cls.wordDict.keys())[randNum]

    @classmethod
    def let_me_check(cls):
        print(f"There are {len(cls.wordDict.keys())} Pva!")

    @classmethod
    def pva(cls):
        for _pva in cls.wordDict.keys():
            print(_pva)

def go():
    print("0:结束\n1:随机获取\n?:查看彩虹屁数量\np:查看当前Pva\n>1:获取>1个彩虹屁")
    while True:
        order = input()
        try:
            if order == "0":
                break
            elif order == "1":
                print(ShaDiao.get_one_p())
            elif order == "?":
                ShaDiao.let_me_check()
            elif order == "p":
                ShaDiao.pva()
            elif int(order) > 1:
                ShaDiao.get_Ps(int(order))
        except:
            print("你打尼玛!")

if __name__ == "__main__":
    go()
