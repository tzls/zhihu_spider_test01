from bs4 import BeautifulSoup
from Utils import *
#
#
soup = BeautifulSoup(open('C:/Users/zhou/Desktop/index.html',encoding='utf-8'),'lxml')
question_item = \
soup.find_all("meta", attrs={"itemprop": "url", "content": re.compile(r'https://www.zhihu.com/question/(\d){8}$')})
names=[]
for question_item_name in question_item:
    name= question_item_name.attrs["content"]
    names.append(name)
print("question_item_name......",name)

#
# s=[["answer",196851952,"read"],["answer",145790972,"read"]]
#
# files={'items':s,
#  }
#
# utils = Utils()
# session = utils.getSession()
#
# header ={
#      'Host':'www.zhihu.com',
#     'Referer':'https://www.zhihu.com/question/55504311',
#    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
# }
# response = session.post('https://www.zhihu.com/lastread/touch',data= files,headers=header)
# print(response)

