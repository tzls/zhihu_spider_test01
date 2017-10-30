from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from Utils import *
from HtmlParser import *

def getDriver():
    utils = Utils()
    htmlParser=HtmlParser()
    driver = webdriver.Chrome()
    driver.get("https://www.zhihu.com/#signin")

    signin_switch_button = driver.find_element_by_class_name("qrcode-signin-cut-button")
    signin_switch_button.click()
    account = driver.find_element_by_name("account")
    password=driver.find_element_by_name("password")
    account.clear()
    password.clear()
    account.send_keys(u"1721984961@qq.com")
    password.send_keys(u"zhou123")
    time.sleep(4)
    signin_button = driver.find_element_by_xpath(".//*[@class='view view-signin']//button[@class='sign-button submit']")
    signin_button.click()

    #https://www.zhihu.com/question/51566232
    driver.get("https://www.zhihu.com/question/55504311")
    time.sleep(4)
    js = 'window.scrollTo(0,document.body.scrollHeight);'
    #QuestionMainAction = driver.find_element_by_xpath(".//button[@class='Button QuestionMainAction']")
    while True:
        driver.execute_script(js)
        time.sleep(2)
        try:
            QuestionMainAction = driver.find_element_by_xpath(".//button[@class='Button QuestionMainAction']")
        except:
            break
    db = utils.getDB('zhihu')
    question_json = htmlParser.parse_question_response(driver.page_source)
    db.questions.insert(question_json)

if __name__=='__main__':
    getDriver()
