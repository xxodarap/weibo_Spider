# -*- coding: UTF-8 –*-
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
import urllib.request

# #
# # url2 = "https://sso-443.e.buaa.edu.cn/login?service=https%3A%2F%2Fcourse.e.buaa.edu.cn%2Fsakai-login-tool%2Fcontainer"
# # cookie2  = {"Cookie": "ga=GA1.3.2090306133.1508731025; Hm_lvt_8edeba7d3ae859d72148a873531e0fa5=1516611381; webvpn_username=paradox%7C1518405302%7C79782245d50e933f525cfe5936275316f8a6fc1c; _astraeus_session=Rmw3b21KZVNsRjgxb3I0em5WZnVHTjYzV3ZUS0pxK0t5REc1VlpMSXlIemg0RzZIK3NHSFptLzhBcE9WSisrRDhJSXhsWlhwNmtWTVEvUStLSFR3WG9RWDJYZUdnR1RKVnlVcnBUcjUrUFJlOWI1aDJ6aDRiZlVoeFEvZk9oU1hidHRoR0g5eThibitlZmlsbThDS0N1TkNrekN0a3l4dDI5V2M0T1NMdCt6SE5LeEFRdW9kQitZVUplU0xHV3NOTTByWEUzVmRxWGVxa2IwTG9TUEtGT09WVHdvNlkxWTRIcEJ2bExkTUZscCtyYll2emdFNkVyYTZlWGVuYU1SVElIdzIxZ3JwMEZrcFVQeTFXRTl2bFdDTEhEQ3lkVGg2QU12cXB0VzRwWHpaRXhZWHBWTFFSRG9Cc1BQbHY1SWN5NVZteTg3UEJ1TkM0V0RSdjNjNEVzMXcvclpnNkhtUTZPZnpZWm5wZzZLZGswdER2MGcrbHlQcHU3WHFoaXNYSG5CV0hBZ3VRN2ljOGgxa09qdytidnR3RktNQmRYTzR5TStPK1JKVnc5RT0tLWlseVdVdnJpSjloaGdFZEtCNzVEVHc9PQ%3D%3D--81269081a871864e5dc08a3581a7671c682fb018; JSESSIONID=4da937ed-ec7b-47ba-8f7f-7c6ed49e7755.couser; CASTGC=TGT-127041-MCCui25DbZ0ODBkIK3vR49fd63wa3coxRNzdam6m7mK6K0f35y-cas"}
# # text2 = requests.get(url2, cookies = cookie2).text
cookie = {"Coolie": "_ga=GA1.3.2090306133.1508731025; Hm_lvt_8edeba7d3ae859d72148a873531e0fa5=1516611381; SERVERID=Server1; webvpn_username=paradox%7C1518405283%7C7d8ef8b9d827f10cccd4809f6507a7bafd4fa0b2; CASTGC=TGT-126984-5fDN5IXucPqVLqQklfbSrnhlJIuZAjJUAo1P6Mowj1P1TlkylO-cas; _astraeus_session=MGYrQld2MmNQZzFKU05BZTZTTFpUMmFjTG5ubGlpRG5QZ0FuVjh0SFdpTW45eU9rK001VUpXTXlENGt3bUxPY2dQVEUvaEhvRHFiU0tRTkRIQ2NYMk1wL09yZS9SRGczRldMcWFBV1ZObTc1RTB2MGc1UlE4ZEtUZ3JEQVl4UzNOSzgzLytjR0thdVUwTXpMRTFLVGVGcWxsWUx1a09KOEl1RjFQWXE5S3VXTERMcEY5eVBiWFJ2M05pUm5wZDlNWTl4ZzY1SENYaG5xaTl3TlhUYUxPTS9lR2ltZU40Nk1JRnZxUVJXcXNhVUlaU3Q1TDhianN3aG10TFJ6c2tzaWR1VWtyc2djNnFqNWJoT21kOGl0WmlwdUdMam1YUHpjTGUzSXMvSHpTUTZSNklMWUk1SkpUR2lNWlRsRmlGZUQtLVgrTmY0TXJGWHV0ZDNrZjIyajlOUHc9PQ%3D%3D--fa978ab70250b7a819626f2c454c3d7dc74ee2c5"}
# # url = "https://course.e.buaa.edu.cn/opencourse/course/detail/12419"
# # text = requests.get(url, cookies = cookie).text
# # print(text)
#
# # url = "https://e.buaa.edu.cn/users/sign_in"
# # cookie = {"Coolie": "_ga=GA1.3.2090306133.1508731025; Hm_lvt_8edeba7d3ae859d72148a873531e0fa5=1516611381; SERVERID=Server1; webvpn_username=paradox%7C1518405283%7C7d8ef8b9d827f10cccd4809f6507a7bafd4fa0b2; CASTGC=TGT-126984-5fDN5IXucPqVLqQklfbSrnhlJIuZAjJUAo1P6Mowj1P1TlkylO-cas; _astraeus_session=MGYrQld2MmNQZzFKU05BZTZTTFpUMmFjTG5ubGlpRG5QZ0FuVjh0SFdpTW45eU9rK001VUpXTXlENGt3bUxPY2dQVEUvaEhvRHFiU0tRTkRIQ2NYMk1wL09yZS9SRGczRldMcWFBV1ZObTc1RTB2MGc1UlE4ZEtUZ3JEQVl4UzNOSzgzLytjR0thdVUwTXpMRTFLVGVGcWxsWUx1a09KOEl1RjFQWXE5S3VXTERMcEY5eVBiWFJ2M05pUm5wZDlNWTl4ZzY1SENYaG5xaTl3TlhUYUxPTS9lR2ltZU40Nk1JRnZxUVJXcXNhVUlaU3Q1TDhianN3aG10TFJ6c2tzaWR1VWtyc2djNnFqNWJoT21kOGl0WmlwdUdMam1YUHpjTGUzSXMvSHpTUTZSNklMWUk1SkpUR2lNWlRsRmlGZUQtLVgrTmY0TXJGWHV0ZDNrZjIyajlOUHc9PQ%3D%3D--fa978ab70250b7a819626f2c454c3d7dc74ee2c5"}
# # text = requests.get(url, cookies = cookie).text
# # print(text)
#
#
# url = "https://course.e.buaa.edu.cn/opencourse/course/detail/12419"
# cookie2  = {"Cookie": "ga=GA1.3.2090306133.1508731025; Hm_lvt_8edeba7d3ae859d72148a873531e0fa5=1516611381; webvpn_username=paradox%7C1518405302%7C79782245d50e933f525cfe5936275316f8a6fc1c; _astraeus_session=Rmw3b21KZVNsRjgxb3I0em5WZnVHTjYzV3ZUS0pxK0t5REc1VlpMSXlIemg0RzZIK3NHSFptLzhBcE9WSisrRDhJSXhsWlhwNmtWTVEvUStLSFR3WG9RWDJYZUdnR1RKVnlVcnBUcjUrUFJlOWI1aDJ6aDRiZlVoeFEvZk9oU1hidHRoR0g5eThibitlZmlsbThDS0N1TkNrekN0a3l4dDI5V2M0T1NMdCt6SE5LeEFRdW9kQitZVUplU0xHV3NOTTByWEUzVmRxWGVxa2IwTG9TUEtGT09WVHdvNlkxWTRIcEJ2bExkTUZscCtyYll2emdFNkVyYTZlWGVuYU1SVElIdzIxZ3JwMEZrcFVQeTFXRTl2bFdDTEhEQ3lkVGg2QU12cXB0VzRwWHpaRXhZWHBWTFFSRG9Cc1BQbHY1SWN5NVZteTg3UEJ1TkM0V0RSdjNjNEVzMXcvclpnNkhtUTZPZnpZWm5wZzZLZGswdER2MGcrbHlQcHU3WHFoaXNYSG5CV0hBZ3VRN2ljOGgxa09qdytidnR3RktNQmRYTzR5TStPK1JKVnc5RT0tLWlseVdVdnJpSjloaGdFZEtCNzVEVHc9PQ%3D%3D--81269081a871864e5dc08a3581a7671c682fb018; JSESSIONID=4da937ed-ec7b-47ba-8f7f-7c6ed49e7755.couser; CASTGC=TGT-127041-MCCui25DbZ0ODBkIK3vR49fd63wa3coxRNzdam6m7mK6K0f35y-cas"}
# text = requests.get(url, cookies = cookie2).text
# print(text)
f = open("wanglei.html", "rb")
html_file = f.read()
# print(type(html_file))
# pdf_url = selector.xpath("/html/body/div[4]/div/div[1]/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[1]/a/@href")
# print(pdf_url)
soup = BeautifulSoup(html_file, "lxml")
# print(soup)
# print(soup.table.a['href'])
pdf_url = []
i = 0
# for pdf in soup.table.find_all('a'):
pdf_file = requests.get("https://course.e.buaa.edu.cn/access/content/group/fd3602fb-bcb2-46d7-b9d6-a2b3eba0a26e/%E8%AE%B2%E4%B9%89/1.%E5%BC%95%E8%AE%BA.pdf", cookies = cookie).content
pdf_soup = BeautifulSoup(pdf_file, "lxml")
print(pdf_soup)
    # urllib.request.urlretrieve(pdf['href'], 'C:/Users/ze/Desktop/spider/pdf/' + pdf.string)

# pdf_url = re.findall('a href=\"(.+\.+pdf)\">', html_file)
# print(pdf_url)
# /html/body/div[4]/div/div[1]/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[1]/a