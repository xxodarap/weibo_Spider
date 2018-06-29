# -*- coding: UTF-8 –*-
from snownlp import SnowNLP

# file = open('C:\\Users\\ze\\Desktop\\5082584680.txt', "r", encoding="utf-8")
# text = file.read()
# print(text)
text = "哈哈 一瞬间恍惚回到了两年前那个被人照顾的小可爱 非主流般的回忆涌上心头 还十分感动"
s = SnowNLP(text)
print(s.sentiments)
tags = [x for x in s.tags]
