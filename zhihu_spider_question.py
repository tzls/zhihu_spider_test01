# -*-coding:utf-8-*-
from Utils import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class zhihu_spider_question():
    def __init__(self):
        self.utils = Utils()
        self.driver = self.utils.getDriver()
        #self.session = self.utils.getSession()
        self.session = requests.session()
        self.old_questions = set()
        self.new_questions = set()
        self.db = self.utils.getDB('zhihu')
        self.header = {
            'HOST': 'www.zhihu.com',
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        }
        self.htmlParser = HtmlParser()

    def spider_now(self):
        while True:
            if self.new_questions and len(self.old_questions) <10:
                # 即将爬取的问题ID
                question_Id = self.new_questions.pop()
                question_Address = 'https://www.zhihu.com%s' % (question_Id)
                self.driver.get(question_Address)
                js = 'window.scrollTo(0,document.body.scrollHeight);'
                # QuestionMainAction = driver.find_element_by_xpath(".//button[@class='Button QuestionMainAction']")
                while True:
                    self.driver.execute_script(js)
                    time.sleep(3)
                    try:
                        QuestionMainAction = self.driver.find_element_by_xpath(
                            ".//button[@class='Button QuestionMainAction']")
                        QuestionMainAction.click()
                    except:
                        break
                #question_title,question_title_details= self.htmlParser.parse_question_response(question_response.text)
                question_json = self.htmlParser.parse_question_response(self.driver.page_source,question_Id)

            else:
                print("爬取结束")
                break
                # 获取数据库
        if question_json is not None:
            self.db.question666.insert(question_json)

if __name__ =='__main__':
    zhihu_spider =zhihu_spider_question()
    zhihu_spider.new_questions.add("/question/66761936")
    zhihu_spider.new_questions.add("/question/23583623")
    zhihu_spider.spider_now()



