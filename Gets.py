# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 21:14:54 2018

@author: fengl
"""
# Ex7_8.py


import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import re
import jieba
import collections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image,ImageSequence
import numpy as np
jieba.setLogLevel(jieba.logging.INFO)



# 获取单独的新闻网页内容
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('utf-8')
    return html

# 获取单独的新闻网页URL
def getnews_herf(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('utf-8')
    tree = etree.HTML(html)
    div_list = tree.xpath('//div[@class="left-content-1 marBot"]/div/ul/li')
    return div_list


# 获取十篇新闻内容
html = "https://news.sina.com.cn/china/"
div_list = getnews_herf(html)

# 打开一个文本文件写入新闻内容。
fp = open('news.txt','w',encoding='utf-8')

# 循环录入每篇新闻内容
i = 0
while True:
    # 循环十次读入十条新闻
    for div in div_list:
        # 从获得的新闻标签列表中分别获得网站
        html1 = div.xpath('./a/@href')[0]
        i += 1
        # 每次获取后，次数加一直到十次。
        html2 = getHtml(html1)
        # 获取具体新闻内容的网站信息。
        bsObj = BeautifulSoup(html2, 'html.parser')
        # 获取网站内的<p>标签内容。
        downloadList = bsObj.select('p')
        # 创建一个空列表，后续存入新闻内容。
        text_list = []
        # 获取符合条件的<p>标签内容。
        text_re = re.compile(r'<p ?(cms-style="font-L")?>(\s+?\S+?)</p>')
        for txt in downloadList:
            html="{}".format(txt)
            # 比较符合条件的p标签内容
            text_list += text_re.findall(html)
            for text_tuple in text_list:
                for x in text_tuple:
                    # 写入内容
                    fp.write(x)
        # 每次写完之后代表一篇新闻结束，换行以表示新一篇新闻开始
        fp.write("\n")
        # 当十次后结束
        if i == 10:
            break
    # 结束最外层循环代表写入完毕
    break
# 关闭文件。
fp.close()



with open('news.txt',encoding='utf-8') as f:
    data = f.read()

# 文本预处理  去除一些无用的字符   只提取出中文出来
new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
new_data = " ".join(new_data)

# 文本分词
seg_list_exact = jieba.cut(new_data, cut_all=True)

result_list = []

for word in seg_list_exact:
    # 设置停用词并去除单个词
    if len(word) > 1:
        result_list.append(word)


# 筛选后统计
word_counts = collections.Counter(result_list)
# 获取前100最高频的词
word_counts_top100 = word_counts.most_common(100)

image= Image.open('ditu.png')#打开背景图
graph = np.array(image)#读取背景图
# 绘制词云
my_cloud = WordCloud(
    background_color='white',  # 设置背景颜色  默认是black
    width=900, height=600,
    max_words=100,            # 词云显示的最大词语数量
    font_path='simhei.ttf',   # 设置字体  显示中文
    max_font_size=99,         # 设置字体最大值
    min_font_size=16,         # 设置子图最小值
    random_state=50,          # 设置随机生成状态，即多少种配色方案
    mask=graph                # 设置背景模板
).generate_from_frequencies(word_counts)

# 显示生成的词云图片
plt.imshow(my_cloud, interpolation='bilinear')
# 显示设置词云图中无坐标轴
plt.axis('off')
plt.show()
my_cloud.to_file('3.png')

