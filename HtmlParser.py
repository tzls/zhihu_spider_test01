#coding:utf-8
from bs4 import  BeautifulSoup
import json
import re
import urllib.request
from scrapy.selector import Selector
#from pybloom import BloomFilter
from BloomFilter import *
class HtmlParser(object):
    def parse_content(self,response):
        #soup = BeautifulSoup(open(response, encoding='utf-8'), 'lxml')
        soup = BeautifulSoup(response.text, 'lxml')
        #用户名
        userName = soup.find("span", class_='ProfileHeader-name').get_text()
        #一句话介绍
        if soup.find("span",class_='RichText ProfileHeader-headline') ==None:
            introduction = None
        else:
             introduction =soup.find("span",class_='RichText ProfileHeader-headline').get_text()
        #居住地
        if len(soup.select('div[class="ProfileHeader-infoItem"]')) == 0 :
            location = None
        else:
            location =soup.select('div[class="ProfileHeader-infoItem"]')[0].get_text("|")
        with open('topic.txt', 'a',encoding="utf-8") as f:
            f.write('用户:%s  一句话介绍:%s  其他相关信息:%s\n' %(userName,introduction,location))
        #我关注的人的总页数
        follower_maxPage = Selector(response).xpath(".//*[@class='Button PaginationButton Button--plain'][last()]/text()").extract()
        if not follower_maxPage :
            follower_maxPage = 1
        else:
            follower_maxPage = int(follower_maxPage.pop())
            if follower_maxPage>3:
                follower_maxPage = 3
        print("follower_maxPage........",follower_maxPage)
        #用户头像
        imageUrl = soup.find("img",class_='Avatar Avatar--large UserAvatar-inner').attrs['src']
        Image_Address = 'C:/Users/zhou/PycharmProjects/zhihu-Test01/Images/%s.jpg' % (userName)
        print("Image_Address.........",Image_Address)
        if imageUrl is not None:
            urllib.request.urlretrieve(imageUrl,Image_Address)

        return userName,introduction,location,Image_Address,follower_maxPage
        # userItem.userName =userItem
        # userItem.introduction = introduction
        # userItem.other_Infos = location
        # userItem.Image_Address = 'C:/Users/zhou/PycharmProjects/zhihu-Test01/Images/%s.jpg' % (userName)


    def parse_User(self,response):
        soup = BeautifulSoup(response, 'lxml')
        #soup = BeautifulSoup(open("C:/Users/zhou/Desktop/index.html", encoding='utf-8'), 'lxml')
        url_temp = soup.find_all("a",attrs={"data-za-detail-view-element_name":"User"})
        us = set()
        users = set()
        for u in url_temp:
            if u in us:
                pass
            else:
                us.add(u)
               # user='https://www.zhihu.com%s/following'%(u.attrs['href'])
                user = u.attrs['href']
                users.add(user)
        return users

    def parse(self,response):
        if response == None:
            return None
        else:
            self.parse_content(response)
            urls = self.parse_url(response)
            return urls

    def parse_asks(self,response):
        soup = BeautifulSoup(response, 'lxml')

        if response is None:
            pass
        else:
            questionHrefs = []
            questionNames = []
            if soup.find("div", class_='QuestionItem-title') is None:
                pass
            else:
                for question_link in soup.find_all("div", class_='QuestionItem-title'):
                    questionHref = question_link.find('a').attrs['href']
                    questionName = question_link.get_text()
                    # questionHrefs = '%s;%s'%(questionHrefs,questionHref)
                    # questionNames = '%s;%s'%(questionNames,questionName)
                    questionNames.append(questionName)
                    print( 'questionNames...........', questionNames)
                return questionNames

    def parse_collections(self, response):
        soup = BeautifulSoup(response, 'lxml')
        if response is None:
            pass
        else:
            collections = []
            if soup.find("div", class_='FavlistItem-title') is None:
                pass
            else:
                collectionNames = []
                for collection_link in soup.find_all("div", class_='FavlistItem-title'):
                    collectionName = collection_link.get_text()
                    # collectionNames = '%s;%s' %(collectionNames,collectionName)
                    collectionNames.append(collectionName)
                    print('collectionNames...........', collectionNames)
                return collectionNames
    #扒取用户关注的人和关注用户的人
    def parse_followers(self, response):
        soup = BeautifulSoup(response, 'lxml')
        follower_names = []
        follower_hrefs = []
        if soup.find_all("span",class_='UserLink UserItem-name') is None:
            pass
        else:
            for soup_link in soup.find_all("span",class_='UserLink UserItem-name'):
                follower_name = soup_link.get_text()
                follower_href = soup_link.find('a').attrs['href']
                follower_names.append(follower_name)
                follower_hrefs.append(follower_href)
            return follower_hrefs,follower_names
    #扒取关注用户的人
    def parse_followee_maxPage(self,response):
        #关注该用户的用户页数
        followee_maxPage = Selector(response).xpath(".//*[@class='Button PaginationButton Button--plain'][last()]/text()").extract()
        if not followee_maxPage:
            followee_maxPage = 1
        else:
            followee_maxPage = int(followee_maxPage.pop())
            if followee_maxPage > 3:
                followee_maxPage = 3
        return followee_maxPage

    def parse_question_response(self,response,question_Id):
        bf = BloomFilter()
        #问题题目
        soup = BeautifulSoup(response, 'lxml')
        question_title = soup.find("div",class_="QuestionPage").find("meta",attrs={"itemprop":"name"}).attrs["content"]
        question_keywords = soup.find("div",class_="QuestionPage").find("meta",attrs={"itemprop":"keywords"}).attrs["content"]
        question_answerCount = soup.find("div",class_="QuestionPage").find("meta",attrs={"itemprop":"answerCount"}).attrs["content"]
        question_title_details=soup.find("div",class_="QuestionRichText--collapsed").find("span").get_text()
        question_List_item = soup.find_all("div",class_="List-item")
        comments = []
        try:
            for q_L_i in question_List_item:
                comment = {}
                # 回答者
                question_item_name = q_L_i.find("meta", attrs={"itemprop": "name"}).attrs["content"]
                # 回答
                question_item_comment = q_L_i.find("span", class_="RichText CopyrightRichText-richText").get_text()
                # 支持人数
                question_item_vote = q_L_i.find("button", class_='Button VoteButton VoteButton--up').get_text()
                comment['回答者'] = question_item_name
                comment['回答'] = question_item_comment
                comment['点赞数'] = question_item_vote

                if bf.isContains(question_Id,comment):
                    print('存在该comment',comment)
                    pass
                else:
                    print('新评论',comment)
                    bf.insert(question_Id,comment)
                    comments.append(comment)
        except:
            pass
        js = {"标题": question_title, "关键字": question_keywords, "回答数": question_answerCount, "问题说明": question_title_details,
              "回答": comments, }
        question_json = json.loads(json.dumps(js, ensure_ascii=False))
        return question_json

    def parse_question_url(self,response):
        question__urls = []
        soup = BeautifulSoup(response, 'lxml')
        question_item_name = soup.find("meta", attrs={"itemprop": "url","content":re.compile('https://www.zhihu.com/question/(\d){8}')}).attrs["content"]
    #寻找根标题(如游戏、运动等)下面的子标题
    def parse_topic_url(self,response):
        soup = BeautifulSoup(response, 'lxml')
        urls = set()
        topic_finds = soup.find_all("a",attrs={"href":re.compile('/topic/(\d){8}')})
        for topic_find in topic_finds:
            topic_url = topic_find.attrs['href']
            urls.add(topic_url)
        return urls

    def parse_topic_question_url(self,response):
        #问题题目
        soup = BeautifulSoup(response, 'lxml')
        question_links_soup = soup.find_all("a",class_='question_link')
        question_links = set()
        for question_link_soup in question_links_soup:
            question_link = question_link_soup.attrs['href']
            question_links.add(question_link)
        return question_links

if __name__ == '__main__':
    zhihu = HtmlParser()
    zhihu.parse_content()
