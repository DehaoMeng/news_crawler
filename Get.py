"""
    本模块内容功能是爬取腾讯新闻网页十篇新闻内容
    Get_news()类是获取新闻网页内容和新闻内容并将文字保存到本地。
"""

import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import re
import tkinter.ttk
from tkinter import ttk
import progressbar


class Get_news(object):
    """
     获取新闻网页内容和新闻内容并将文字保存到本地
    """
    def __init__(self):
        """ 初始化该类 """
        self.html = "https://news.sina.com.cn/china/" # 新闻网址
        self.div_list = self.getnews_herf(self.html) # 调用函数获取新闻网页中的url。
        self.write_news(self.div_list)

    def getnews_herf(self,url):
        """
         获取网页中具体新闻的url
         """
        html = urllib.request.urlopen(url).read()
        html = html.decode('utf-8')
        tree = etree.HTML(html)
        div_list = tree.xpath('//div[@class="left-content-1 marBot"]/div/ul/li')
        return div_list

    def get_html(self,url):
        """
        获取具体新闻网页的内容
        """
        html = urllib.request.urlopen(url).read()
        html = html.decode('utf-8')
        return html

    def write_news(self,div_list):
        """
         读取具体新闻并将新闻写入文本文件中
         """
        # 打开一个文本文件写入新闻内容。
        # 这里要改为excel表格或者数据库形式存入。
        fp = open('news.txt','w',encoding='utf-8')
        # 循环录入每篇新闻内容
        i = 0
        while True:
            # 循环十次读入十条新闻
            for div in div_list:
                # 从获得的新闻标签列表中分别获得网站
                html1 = div.xpath('./a/@href')[0]
                # print(html1)
                i += 1
                # 每次获取后，次数加一直到十次。
                html2 = self.get_html(html1)
                # 获取具体新闻内容的网站信息。
                bsObj = BeautifulSoup(html2, 'html.parser')
                # 获取网站内的<p>标签内容。
                downloadList = bsObj.select('p')
                # 创建一个空列表，后续存入新闻内容。
                text_list = []
                # 获取符合条件的<p>标签内容。
                text_re = re.compile(r'<p ?(cms-style="font-L")?>(\s+?\S+?)</p>')
                # print(downloadList)
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

if __name__ == "__main__":
    Get_news()