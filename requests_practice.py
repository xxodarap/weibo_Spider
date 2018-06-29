# -*- coding: UTF-8 –*-
# http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
import requests

r = requests.get('https://github.com//')
print(r.text)

# payload = {'key1' : 'value1', 'key2' : ['value2', 'value3']}
# r = requests.get('http://httpbin.org/get', params = payload)
# print(r.url)

