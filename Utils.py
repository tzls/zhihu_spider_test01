import pymongo
from HtmlParser import *
from Utils import *
import requests
import time
import json

from selenium import webdriver
class Utils():

    def getDB(self,dbName):
        client = pymongo.MongoClient('localhost',27017)
        db =client[dbName]
        return db

    def getSession(self):
        header = {
            'HOST': 'www.zhihu.com',
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        }
        session = requests.session()
        # 未爬取的url
        new_users = set()
        # 已爬取的url
        old_users = set()
        htmlParser = HtmlParser()

        response = session.get('https://www.zhihu.com', headers= header)
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract_first()
        # 验证码URL是按照时间戳的方式命名的
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time() * 1000))
        response_s =  session.get(captcha_url, headers= header)
        # 验证码URL是按照时间戳的方式命名的
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time() * 1000))
        response_s =  session.get(captcha_url, headers= header)
        # 保存验证码到当前目录
        with open('captcha.gif', 'wb') as f:
            f.write(response_s.content)
            f.close()
        # 自动打开刚获取的验证码
        from PIL import Image
        try:
            img = Image.open('captcha.gif')
            img.show()
            img.close()
        except:
            pass
        captcha = {
            'img_size': [200, 44],
            'input_points': [],
        }
        points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20],
                  [129.796875, 22],
                  [150.796875, 22]]
        seq = input('请输入倒立字的位置\n>')
        for i in seq:
            captcha['input_points'].append(points[int(i) - 1])
        _captcha = json.dumps(captcha)

        # 开始登录
        post_data = {
            'captcha_type': 'cn',
            '_xsrf': xsrf,
            'email': '1721984961@qq.com',
            'password': 'zhou123',
            'captcha': _captcha,
        }
        response_text =  session.post('https://www.zhihu.com/login/email', data=post_data, headers= header)
        text_json = json.loads(response_text.text)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            print('登录成功')
        return session

    def getDriver(self):
        utils = Utils()
        htmlParser = HtmlParser()
        #driver = webdriver.Chrome()
        #driver = webdriver.PhantomJS('phantomjs')
        driver =webdriver.Firefox()
        driver.get("https://www.zhihu.com/#signin")

        signin_switch_button = driver.find_element_by_class_name("qrcode-signin-cut-button")
        signin_switch_button.click()
        account = driver.find_element_by_name("account")
        password = driver.find_element_by_name("password")
        account.clear()
        password.clear()
        account.send_keys(u"1721984961@qq.com")
        password.send_keys(u"zhou123")
        time.sleep(7)
        signin_button = driver.find_element_by_xpath(
            ".//*[@class='view view-signin']//button[@class='sign-button submit']")
        signin_button.click()
        time.sleep(2)
        return driver

    
