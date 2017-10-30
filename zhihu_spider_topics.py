# -*- coding:utf-8 -*-
from HtmlParser import *
from Utils import  *

class zhihu_spider_topics(object):
    def __init__(self):
        self.htmlParser = HtmlParser()
        self.utils = Utils()
        self.old_topic_urls =set()
        self.new_topic_urls =set()
        self.old_topic_question_urls =set()#存放所有已爬过的问题URL,如https://www.zhihu.com/question/48847850

    def spider_now(self):
        self.driver = self.utils.getDriver()
        self.driver.get("https://www.zhihu.com/topics")
        time.sleep(3)
        #url_topics = self.htmlParser.parse_topic_url(self.driver.page_source)
        url_topics=[]
        url_topics.append('/topic/19579244/top-answers')
        for url in url_topics:
            self.new_topic_urls.add(url)
        while True:
            if self.new_topic_urls and len(self.old_topic_urls) < 2:
                print("wolegequ")
                url_topic = self.new_topic_urls.pop()
                url_topic_all = 'https://www.zhihu.com%s' % (url_topic)
                print("url_topic.........",url_topic_all)
                self.driver.get(url_topic_all)
                time.sleep(2)
                self.old_topic_urls.add(url_topic)
                topic_questions = self.htmlParser.parse_topic_question_url(self.driver.page_source)
                for topic_question in topic_questions:
                    if topic_question not in self.old_topic_question_urls:
                        url_topic_question = 'https://www.zhihu.com%s' % (topic_question)
                        print("url_topic_question.....", url_topic_question)
                        self.old_topic_question_urls.add(topic_question)
                        self.driver.get(url_topic_question)
                        time.sleep(2)
                        js = 'window.scrollTo(0,document.body.scrollHeight);'
                        # QuestionMainAction = driver.find_element_by_xpath(".//button[@class='Button QuestionMainAction']")
                        while True:
                            self.driver.execute_script(js)
                            time.sleep(3)
                            try:
                                QuestionMainAction = self.driver.find_element_by_xpath( ".//button[@class='Button QuestionMainAction']")
                            except:
                                break
                        question_json = self.htmlParser.parse_question_response(self.driver.page_source)
                        # 获取数据库
                        db = self.utils.getDB('zhihu')
                        db.zhoudong.insert(question_json)
                    else:
                        pass
            else:
                print('爬取结束')
                self.driver.close()
                break

if __name__ =='__main__':
    zhihu_spider =zhihu_spider_topics()
    #zhihu_spider.new_users.add("/people/tzls")
    zhihu_spider.spider_now()


