# -*- coding:utf-8 -*-
import pymongo
import json
from Utils import *
from HtmlParser import *
class Zhihu_Spider(object):

    def __init__(self):
        self.utils = Utils()
        self.session = self.utils.getSession()
        self.new_users = set()
        self.old_users = set()
        self.header = {
            'HOST': 'www.zhihu.com',
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        }
        self.htmlParser = HtmlParser()

    def spider_now(self):
        while True:
            if self.new_users is not None and len(self.old_users) < 5:
                #即将爬取的用户ID
                user_spider = self.new_users.pop()
                user_following = 'https://www.zhihu.com%s/following' % (user_spider)
                response_following = self.session.get(user_following, headers=self.header)

                userName, introduction, location, Image_Address,follower_maxPage= self.htmlParser.parse_content(response_following)
                #爬取该用户关注的人
                follower_names_total = []
                for pageIndex in range(1,follower_maxPage+1):
                    user_follower = 'https://www.zhihu.com%s/following?page=%s' % (user_spider,pageIndex)
                    response_follower = self.session.get(user_follower, headers=self.header)
                    follower_hrefs, follower_names=self.htmlParser.parse_followers(response_follower.text)
                    follower_names_total.extend(follower_names)
                    for follower_href in follower_hrefs:
                        if follower_href not in self.old_users:
                            self.new_users.add(follower_href)

                #爬取关注该用户的人
                followee_names_total = []
                user_followee1 = 'https://www.zhihu.com%s/followers' %(user_spider)
                response_followee1=self.session.get(user_followee1, headers=self.header)
                followee_maxPage = self.htmlParser.parse_followee_maxPage(response_followee1)
                for pageIndex in range(1, followee_maxPage + 1):
                    user_followee = 'https://www.zhihu.com%s/followers?page=%s' % (user_spider, pageIndex)
                    response_follower = self.session.get(user_followee, headers=self.header)
                    followee_hrefs, followee_names = self.htmlParser.parse_followers(response_follower.text)
                    followee_names_total.extend(followee_names)
                    for followee_href in followee_hrefs:
                        if followee_href not in self.old_users:
                            self.new_users.add(followee_href)

                #爬取用户提问页面
                user_asks = 'https://www.zhihu.com%s/asks' % (user_spider)
                response_asks = self.session.get(user_asks,headers=self.header)
                questionNames =  self.htmlParser.parse_asks(response_asks.text)
                #爬取用户收藏页面
                user_collections = 'https://www.zhihu.com%s/collections' % (user_spider)
                response_collections = self.session.get(user_collections,headers =self.header)
                collections = self.htmlParser.parse_collections(response_collections.text)
                js={"用户名":userName,"一句话介绍":introduction,"其他信息":location,"头像地址":Image_Address,"提问问题":questionNames,
                    "收藏":collections,"我关注的人":follower_names_total,"关注我的人":followee_names_total}
                insert_user=json.loads(json.dumps(js,ensure_ascii=False))
                print("insert_user",insert_user)
                #获取数据库
                db = self.utils.getDB('zhihu')
                db.collection.insert(insert_user)
                self.old_users.add(user_spider)
                print("已经爬取%s个用户"%(len(self.old_users)))
            else:
                print("爬取结束")
                break

if __name__ =='__main__':
    zhihu_spider =Zhihu_Spider()
    zhihu_spider.new_users.add("/people/tzls")
    zhihu_spider.spider_now()