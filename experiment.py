import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
import sys

cookie = {"Cookie": "_T_WM=785b304358e8d7ffc810967091d7de37; SUB=_2A253oLJVDeRhGeBO7FUU-S_Iyz2IHXVVat4drDV6PUJbkdAKLXntkW1NRa4tr4TxrHRniCd56Hb6fW24iDuymbtC; SUHB=03oFD-WU6vLuZ4; SCF=Ao4ziTsjeUH6yWFsFJ2bkIl9Ud7Ln6bfwh9zoatMUPGnrPCcxD1lZyl_VOwRVIrCZ0_P4WHrkYXKKicW8yHLxdc.; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword; SSOLoginState=1520747013"}

# url = "https://weibo.cn/u/5082584680?filter=1&page=1"
# text = requests.get(url, cookies = cookie).text
# soup = BeautifulSoup(text, "lxml")
#
# username = soup.title.text[:-3]
#
# following = soup.find(attrs = {'class' : 'tip2'}).text.split( )[:-2]
# print(following)
# print("用户名：" + username)
weibo_content = []
url = "https://weibo.cn/u/5082584680?filter=1&page=1"
content = requests.get(url, cookies = cookie).content
selector = etree.HTML(content)
for i in range(3, 13):
    number = i * 2 + 1
    url_child = selector.xpath("/html/body/div[%d]/div[2]/a[1]/@href" % number)
    if url_child == []:
        continue
    else:
        print(url_child)






