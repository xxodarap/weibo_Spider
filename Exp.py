import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
import time

url = "http://top.aiweibang.com/article/L8O9MMOmw6zCtw~~"
driver = webdriver.PhantomJS(executable_path="E:\\phantomjs-2.1.1-windows\\bin\\phantomjs")
driver.get(url)
for i in range(2):
    # print(driver.page_source)
    driver.find_element_by_xpath("/html/body/section/div[2]/div[1]/div/div/div[5]/div[3]/div/a[10]").click()
