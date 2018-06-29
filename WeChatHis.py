import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
import time


# url = "http://top.aiweibang.com/article/L8O9MMOmw6zCtw~~"
# driver = webdriver.PhantomJS(executable_path="E:\\phantomjs-2.1.1-windows\\bin\\phantomjs")
# driver.get(url)
# text = driver.page_source
# print(text)

text = open("./11111.html", "r", encoding="utf-8").read()
content = text.encode("utf-8")
selector = etree.HTML(content)

soup = BeautifulSoup(text, "lxml")

# articleName = (soup.find_all(attrs = {'class' : 'articleName'}))
# for article in articleName:
#     print(article)
#
# ArticleNamePool = []
# soup.find_all(attrs={'class' : 'articleName'})
# for articleName in ArticleNamePool:
#     print(articleName)


ArticleTimePool = []
AritcleNamePool = []
ChildUrlPool = []

for i in range(1, 21):
    try:
        ChildUrl = selector.xpath("/html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[%d]/a/@href" % i)
        AritcleName = selector.xpath("/html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[%d]/a/text()" % i)
        ArticleTime = selector.xpath("/html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[%d]/div[1]/text()" % i)
        AritcleNamePool.append(AritcleName)
        ArticleTimePool.append(ArticleTime)
        # ChildUrlPool.append(ChildUrl[0])
        ChildUrlPool.append("http://top.aiweibang.com/" + ChildUrl[0])
        # print(AritcleName[0])
    except:
        continue

for i in range(0, 20):
    try:
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        # print(AritcleNamePool[i])
        # print(ChildUrlPool[i])
        # text= requests.get(ChildUrlPool[i]).text
        # print(text)
        # ChildUrlSoup = BeautifulSoup(text, "lxml")
        # print(ChildUrlSoup.find_all(attrs={'class':'profile_meta_value'})[1].get_text())
        driver = webdriver.Firefox(firefox_options=fireFoxOptions)
        driver.get(ChildUrlPool[i])
        print(driver.page_source)
        # driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click()
        # print(type(driver.page_source))
        # ChildContent = ChildText.encode("utf-8")
        # ChildSelector = etree.HTML(ChildContent)
        # ChildSoup = BeautifulSoup(driver.page_source, "lxml")
        # print(ChildSoup)
        # print(ChildSoup.p)
        break
    except:
        continue


# http://top.aiweibang.com/
# /html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[1]/a
# /html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/a
# /html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[20]/a
# /html/body/div[1]/div/div[1]/div[1]/div[2]/p[4]
# /html/body/div[1]/div/div[1]/div[1]/div[2]/p[1]
# //html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[1]/div[1]
# /html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[6]/div[1]

# /html/body/section/div[2]/div[1]/div/div/div[5]/div[2]/div[1]/a

# /html/body/section/div[2]/div[1]/div/div/div[5]/div[3]/div/a[1]
# /html/body/section/div[2]/div[1]/div/div/div[5]/div[3]/div/a[10]
# /html/body/section/div[2]/div[1]/div/div/div[5]/div[3]/div/a[10]