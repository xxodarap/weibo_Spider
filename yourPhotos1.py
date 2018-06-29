import re
import requests
from bs4 import BeautifulSoup
from lxml import etree

cookie = {"Cookie": "_T_WM=785b304358e8d7ffc810967091d7de37; SUB=_2A253mvvUDeRhGeBO7FUU-S_Iyz2IHXVVZIWcrDV6PUJbkdAKLUXykW1NRa4trw64fEPUszF6YJYL_SQ7QO-lFpWq; "
                    "SUHB=0pHx0htKsbxOaf; SCF=Ao4ziTsjeUH6yWFsFJ2bkIl9Ud7Ln6bfwh9zoatMUPGnrPCcxD1lZyl_VOwRVIrCZ0_P4WHrkYXKKicW8yHLxdc.; SSOLoginState=1520339845"}

url = "https://weibo.cn/mblog/pic/G5IsntH73?rl=0"
content = requests.get(url, cookies = cookie).content
text = requests.get(url, cookies = cookie).text
soup = BeautifulSoup(text, "lxml")
# selector = etree.HTML(content)
# url_next = selector.xpath("//*[@id=\"dummybodyid\"]/div[4]/a/@href")
# print(url_next)


