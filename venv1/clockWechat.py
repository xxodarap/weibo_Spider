import itchat
import time
Wchat = itchat.auto_login(hotReload=True)
friends = itchat.get_friends()[0:]
friends_name = {}
for i in friends:
    if i["RemarkName"]:
        if i["RemarkName"] not in friends_name:
            friends_name[i["RemarkName"]] = i["UserName"]

text = "乌有乡生日快乐！[蛋糕]\n你又开始了一年中长达3个月的年龄压制\n" \
       "虽然对于你们大多数成年人来说 生日的意义被不断淡化\n" \
       "但其实 每年总会有那么几天 被我们用来感恩相遇\n" \
       "人的一生中 也总会有那么几天 被悄悄赋予意义\n" \
       "我一直都有一个不大不小浪漫而又非主流的愿望 就是将来能在属于自己的地方\n" \
       "种上一片风信子 蓝色粉色还有紫色\n" \
       "而难忘的不是因为\"我太念念才难忘\"\n" \
       "是它曾经被赋予过轻如褶皱纸的意义\n" \
       "（我一定是第一个准时发送的[奋斗]，因为我写了个程序哈哈哈，生日快乐！）"

while True:
    time_now = time.strftime('%H%M',time.localtime(time.time()))
    if int(time_now) == 0000:
        itchat.send(text, friends_name["乌有乡"])
        time.sleep(60)
        break
