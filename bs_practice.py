# -*- coding: UTF-8 –*-

from bs4 import BeautifulSoup
import re
import requests
from lxml import etree

# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
#
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
#
# <p class="story">...</p>
# """
# soup = BeautifulSoup(html_doc, "lxml")
#
# # print(soup.prettify())
# print(soup.title)
# print(soup.title.string)
# print(soup.title.parent.name)
# print(soup.p)
# print(soup.p['class'])
# print(soup.a)
# print(soup.find_all('a'))
# for tag in soup.find_all(True):
#     print(tag.name)
#
# for tag in soup.find_all(re.compile("^b")):
#     print(tag.name)
i = 0

url = "https://weibo.cn/u/5082584680?filter=1&page=1"
cookie = {"Cookie": "_T_WM=785b304358e8d7ffc810967091d7de37; SUB=_2A253e8qMDeRhGeBO7FUU-S_Iyz2IHXVUh9bErDV6PUJbkdANLUjEkW1NRa4tr09e0Ka6S27XH9GYbX69KfJKXg6F; SUHB=0IIVE_euwgNUMM; SCF=Ao4ziTsjeUH6yWFsFJ2bkIl9Ud7Ln6bfwh9zoatMUPGnrPCcxD1lZyl_VOwRVIrCZ0_P4WHrkYXKKicW8yHLxdc.; SSOLoginState=1518320348"}
content = requests.get(url, cookies = cookie).content
selector = etree.HTML(content)
url_pool = []
img_url_pool = []
for i in range (3, 12):
    number = i * 2
    url_child = selector.xpath("/html/body/div[%d]/div[2]/a[1]/@href" % number)
    url_pool.append(url_child)
# print(url_pool)


# text = requests.get(url_pool[1][0], cookies = cookie).text
# # print(text)
# img_url = re.findall('src=\"(.+\.+jpg)\"', text)
# # print(img_url)

for url_child in url_pool:
    if url_child == []:
        continue
    else:
        text = requests.get(url_child[0], cookies = cookie).text
        img_url = re.findall('src=\"(.+\.+jpg)\"', text)
        # img_url_pool.append(img_url)
        pic = requests.get(img_url[0])
        fp = open('C:/Users/ze/Desktop/spider/picture1/' + str(i) + '.jpg', 'wb')
        fp.write(pic.content)
        fp.close()
        i = i + 1