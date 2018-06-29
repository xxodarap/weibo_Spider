import re
import requests
from bs4 import BeautifulSoup
from lxml import etree

page_number = 1
number = 0
# img_url = []
for page_number in range(1, 2):
    url = "https://alpha.wallhaven.cc/toplist?page=%d" % (page_number)
    content = requests.get(url).content
    selector = etree.HTML(content)
    for img_number in range(1, 25):
        img = selector.xpath("//*[@id=\"thumbs\"]/section/ul/li[%d]/figure/a/@href" % (img_number))
        img_content = requests.get(img[0]).content
        img_selector = etree.HTML(img_content)
        # // *[ @ id = "wallpaper"]
        img_url = img_selector.xpath("//*[@id=\"wallpaper\"]/@src")
        pic = requests.get('http:' + img_url[0])
        fp = open('E:/PHOTO/wallpaper/' + str(number) + '.jpg', 'wb')
        fp.write(pic.content)
        fp.close()
        number += 1
