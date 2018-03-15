# -*- coding: UTF-8 –*-
import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from lxml import etree
from snownlp import SnowNLP

class Weibo:
    cookie = {"Cookie": ""}

    def __init__(self, user_id, filter = 1):
        self.user_id = user_id
        self.filter = filter
        self.username = ''
        self.weibo_num = ''   # 用户全部微博数
        # self.weibo_num2 = 0 # 爬取到的微博数
        self.following = ''
        self.followers = ''
        self.weibo_content =[]
        self.publish_time = []
        self.up_num = []
        self.retweet_num = []
        self.comment_num = []

    def get_user_info(self):
        url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
            self.user_id, self.filter) # 基本页设定
        text = requests.get(url, cookies = self.cookie).text # 发送包含cookie的请求，返回html文本信息
        soup = BeautifulSoup(text, "lxml") # 用Beautiful中lxml解析器解析，形成标准格式
        username = soup.title.text
        self.username = username[:-3]
        print("用户名[" + self.username + "]")

        info = soup.find(attrs = {'class' : 'tip2'}).text.split()[:-2]
        # 返回的字符串包含了微博数、关注数和粉丝数，因此进行split处理

        self.weibo_num = info[0]
        self.following = info[1]
        self.followers = info[2]

        print(self.weibo_num)
        print(self.following)
        print(self.followers)

    def get_weibo_info(self):
        url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
            self.user_id, self.filter)
        html = requests.get(url, cookies = self.cookie).content
        selector = etree.HTML(html)
        if selector.xpath("//input[@name='mp']") == []:
            page_num = 1 # 由于只有1页的微博，没有总页码的显示，因此要进行特特判
        else:
            page_num = (int)(selector.xpath(
                "//input[@name='mp']")[0].attrib["value"])
        senti_list = [] # 微博情绪值列表
        date_list = [] # 标准时间数据列表
        cnt_0 = 0 # 情绪低落个数
        cnt_1 = 0 # 情绪一般个数
        cnt_2 = 0 # 情绪较好个数
        cnt_3 = 0 # 情绪很好个数

        for page in range(1, page_num + 1):
            every_url = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
            every_text = requests.get(every_url, cookies = self.cookie).text
            every_soup = BeautifulSoup(every_text, "lxml") # 为每一个页面创建Beautifulsoup对象
            self.weibo_content.extend(every_soup.find_all(attrs = {'class': 'ctt'})) # 将每一页的数据添加进数组
            self.publish_time.extend(every_soup.find_all(attrs = {'class': 'ct'}))

            every_content = requests.get(url, cookies = self.cookie).content
            every_selector = etree.HTML(every_content)    # 为每一个页面创建解析树
            info = every_selector.xpath("//div[@class='c']")
            pattern = r"\d+\.?\d*"  # 提取文本中数字的正则

            if len(info) > 3:
                for i in range(0, len(info) - 2):
                    # 获取每条微博的点赞数
                    str_zan = info[i].xpath("div/a/text()")[-4]
                    guid = re.findall(pattern, str_zan, re.M)
                    up_num = int(guid[0])
                    self.up_num.append(up_num)

                    # 获取每条微博的转发数
                    retweet = info[i].xpath("div/a/text()")[-3]
                    guid = re.findall(pattern, retweet, re.M)
                    retweet_num = int(guid[0])
                    self.retweet_num.append(retweet_num)

                    #获取每条微博的评论数
                    comment = info[i].xpath("div/a/text()")[-2]
                    guid = re.findall(pattern, comment, re.M)
                    comment_num = int(guid[0])
                    self.comment_num.append(comment_num)

        cnt = 1 # 微博的编号
        index = 0 # 需要更新的热点微博的索引
        max = 0
        cnt_x = [] # 编号列表
        heat_y = [] # 热度列表

        # 将一天二十四小时等量划分为十二个时间段，创建以下十二个变量
        time0_2 = 0
        time2_4 = 0
        time4_6 = 0
        time6_8 = 0
        time8_10 = 0
        time10_12 = 0
        time12_14 = 0
        time14_16 = 0
        time16_18 = 0
        time18_20 = 0
        time20_22 = 0
        time22_0 = 0

        # 打开文件用于将抓取到的数据写入本地文件，编码方式"utf-8"，更好的显示中文
        f = open("C:\\Users\\ze\\Desktop\\test.txt", "w", encoding='utf-8')

        for speech, time, up, retweet, comment in zip(self.weibo_content[2:], self.publish_time,
                                                      self.up_num, self.retweet_num, self.comment_num):
            # 用snowNLP库中的s.sentiments方法来评估每条微博正面情绪的概率
            sentiments = SnowNLP(speech.text).sentiments

            print(str(cnt) + ":")
            f.write(str(cnt) + ":\n")
            cnt_x.append(cnt)
            heat_y.append((up + retweet + comment) / 1000)
            print("微博内容：" + str(speech.text))
            print("情绪值：" + str(sentiments))
            print("点赞数：" + str(up))
            print("转发数：" + str(retweet))
            print("评论数：" + str(comment))
            f.write(u"微博内容：" + str(speech.text) + "\n")
            f.write(u"情绪值：" + str(sentiments) + "\n")
            f.write(u"点赞数：" + str(up) + "\n")
            f.write(u"转发数：" + str(retweet) + "\n")
            f.write(u"评论数：" + str(comment) + "\n")

            # 统计最高热度的微博是哪条
            if up + retweet + comment > max:
                index = cnt
                max = up + retweet + comment

            cnt += 1

            # 记录情绪值，形成列表，便于绘制图片
            senti_list.append(sentiments)

            # 将概率的大小划分为四个等级，作为四种不同的情绪
            if sentiments < 0.25:
                cnt_0 += 1
            elif sentiments < 0.5:
                cnt_1 += 1
            elif sentiments < 0.75:
                cnt_2 += 1
            else:
                cnt_3 += 1

            print(time.text.split()[0], time.text.split()[1] + '\n')
            f.write(time.text.split()[0]+ " " + time.text.split()[1] + '\n')

            TIME = str(time.text.split()[1])

            # 统计每个时间段的总发布量
            if '00:00' <= TIME and TIME < '02:00':
                time0_2 += 1
            elif '02:00' <= TIME and TIME < '04:00':
                time2_4 += 1
            elif '04:00' <= TIME and TIME < '06:00':
                time4_6 += 1
            elif '06:00' <= TIME and TIME < '08:00':
                time6_8 += 1
            elif '08:00' <= TIME and TIME < '10:00':
                time8_10 += 1
            elif '10:00' <= TIME and TIME < '12:00':
                time10_12 += 1
            elif '12:00' <= TIME and TIME < '14:00':
                time12_14 += 1
            elif '14:00' <= TIME and TIME < '16:00':
                time14_16 += 1
            elif '16:00' <= TIME and TIME < '18:00':
                time16_18 += 1
            elif '18:00' <= TIME and TIME < '20:00':
                time18_20 += 1
            elif '20:00' <= TIME and TIME < '22:00':
                time20_22 += 1
            else:
                time22_0 += 1

            tlist = re.findall(r'\d+\.?\d*', time.text.split()[:-1][0]) # 将时间格式化
            date = []
            if len(tlist) == 2 :
                date.append('2018/' + tlist[0] + '/' + tlist[1])
                # print(t)
                # 将时间标准格式化，便于绘图
                date = pd.to_datetime(date)
                # print(t)
                date_list.append(date)
            elif len(tlist) == 3 :
                date.append(tlist[0] + '/' + tlist[1] + '/' + tlist[2])
                # print(t)
                date = pd.to_datetime(date)
                # print(t)
                date_list.append(date)

        f.close()
        print(index)
        print(self.weibo_content[index+2].text)

        # 情绪分布圆饼图
        # plt.style.use('ggplot')
        # data = [cnt_0, cnt_1, cnt_2, cnt_3]
        # labels = ['sad', 'not good', 'not bad', 'happy']
        # explode = [0, 0, 0, 0.1]
        # colors = ['#F0FFFF','#B0C4DE','#FFF0F5','#FFFFE0']
        #
        # plt.rcParams['axes.unicode_minus'] = False
        #
        # plt.axes(aspect='equal')
        #
        # plt.xlim(0, 4)
        # plt.ylim(0, 4)
        #
        # plt.pie(x=data,  # 绘图数据
        #         explode=explode,  # 突出显示大专人群
        #         labels=labels,  # 添加教育水平标签
        #         colors=colors,  # 设置饼图的自定义填充色
        #         autopct='%.1f%%',  # 设置百分比的格式，这里保留一位小数
        #         pctdistance=0.8,  # 设置百分比标签与圆心的距离
        #         labeldistance=1.15,  # 设置教育水平标签与圆心的距离
        #         startangle=180,  # 设置饼图的初始角度
        #         radius=1.5,  # 设置饼图的半径
        #         counterclock=False,  # 是否逆时针，这里设置为顺时针方向
        #         wedgeprops={'linewidth': 1.5, 'edgecolor': 'green'},  # 设置饼图内外边界的属性值
        #         textprops={'fontsize': 12, 'color': 'k'},  # 设置文本标签的属性值
        #         center=(1.8, 1.8),  # 设置饼图的原点
        #         frame=1)  # 是否显示饼图的图框，这里设置显示
        #
        # plt.xticks(())
        # plt.yticks(())
        #
        # plt.title('Haoran Liu\'s Emotional Map')
        # plt.savefig('E:/Emotional_Map.jpg')
        # plt.show()

        # 作息规律饼图
        # plt.style.use('ggplot')
        # data = [time0_2, time8_10, time10_12, time12_14, time14_16, time16_18, time18_20, time20_22, time22_0]
        # labels = ['00:00-02:00', '08:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00', '18:00-20:00', '20:00-22:00', '22:00-00:00']
        # explode = [0, 0, 0, 0, 0, 0, 0, 0.1, 0]
        # colors = ['#F0F8FF','#F5F5DC','#5F9EA0','#00FFFF', '#FF1493', '#B22222', '#FFD700', '#FFFFF0', '#90EE90', '#00FF00', '#000080', '#FFA500']
        #
        # plt.rcParams['axes.unicode_minus'] = False
        #
        # plt.axes(aspect='equal')
        #
        # plt.xlim(0, 4)
        # plt.ylim(0, 4)
        #
        # plt.pie(x=data,  # 绘图数据
        #         explode=explode,  # 突出显示大专人群
        #         labels=labels,  # 添加教育水平标签
        #         colors=colors,  # 设置饼图的自定义填充色
        #         autopct='%.1f%%',  # 设置百分比的格式，这里保留一位小数
        #         pctdistance=0.8,  # 设置百分比标签与圆心的距离
        #         labeldistance=2.0,  # 设置教育水平标签与圆心的距离
        #         startangle=180,  # 设置饼图的初始角度
        #         radius=1.5,  # 设置饼图的半径
        #         counterclock=False,  # 是否逆时针，这里设置为顺时针方向
        #         wedgeprops={'linewidth': 1.5, 'edgecolor': 'green'},  # 设置饼图内外边界的属性值
        #         textprops={'fontsize': 12, 'color': 'k'},  # 设置文本标签的属性值
        #         center=(1.8, 1.8),  # 设置饼图的原点
        #         frame=1)  # 是否显示饼图的图框，这里设置显示
        #
        # plt.xticks(())
        # plt.yticks(())
        #
        # plt.title('Haoran Liu\'s Daily Schedule')
        # plt.savefig('E:/Haoran Liu\'s Daily Schdule')
        # plt.show()

        # 情绪变化折线图
        # print(date_list)
        # print(len(date_list))
        # print(len(senti_list))
        # plt.plot(date_list, senti_list, color = "springgreen", linewidth = 1.0)
        # plt.savefig('E:/Emotional Run Chart.jpg')
        # plt.title('Haoran Liu\'s Emotional Run Chart')
        # plt.gcf().autofmt_xdate()
        # plt.xlabel("date")
        # plt.ylabel("sentiments")
        # plt.ylim(-1, 2)
        # plt.show()

        # 微博热度折线图
        # plt.plot(cnt_x, heat_y, 'ro')
        # plt.xlabel("index")
        # plt.ylabel("heat")
        # plt.title("heat run chart")
        # plt.ylim(500,2000)
        # plt.show()

    def get_images(self):
        url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
            self.user_id, self.filter)
        html = requests.get(url, cookies=self.cookie).content
        selector = etree.HTML(html)
        if selector.xpath("//input[@name='mp']") == []:
            page_num = 1
        else:
            page_num = (int)(selector.xpath(
                "//input[@name='mp']")[0].attrib["value"])
        img_number = 0
        for page in range(1, page_num + 1):
            url = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                self.user_id, self.filter, page)
            content = requests.get(url, cookies = self.cookie).content
            try:
                selector = etree.HTML(content)
            except:
                continue
            # url_pool = []
            # img_url_pool = []
            for i in range(5, 26):
                number = i
                url_child = selector.xpath("/html/body/div[%d]/div[2]/a[1]/@href" % number) # 获取二级链接
                if url_child == []:
                    continue
                else:
                    print(url_child[0])
                    text = requests.get(url_child[0], cookies = self.cookie).text # 向二级链接发送请求
                    img_url = re.findall('src=\"(.+\.+jpg)\"', text)  # 通过正则表达式 提取网页中的所有jpg链接
                    if img_url == []:
                        continue
                    else:
                        pic = requests.get(img_url[0])
                    fp = open('E:/PHOTO/images/' + str(img_number) + '.jpg', 'wb') # 将图片下载保存到本地
                    fp.write(pic.content)
                    fp.close()
                    img_number += 1

    def start(self):
        self.get_user_info()
        self.get_weibo_info()
        self.get_images()
        print("图片成功抓取")
        print("======================================================================================")

def main():
    user_id = 2870450862 #刘昊然
    filter = 1
    wb = Weibo(user_id, filter)
    wb.start()

if __name__ == '__main__':
    main()
