"""
    本模块内容功能是爬取腾讯新闻网页十篇新闻内容
    Get_news()类是获取新闻网页内容和新闻内容并将文字保存到本地。
"""
import asyncio
from aiohttp import ClientSession
import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import re
import tkinter.ttk
from tkinter import ttk
import progressbar
import time
import warnings
warnings.filterwarnings("ignore")
import logging

logger = logging.getLogger('pencil')
logger.setLevel(level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level = logging.DEBUG)
log_path='log.txt'
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(log_path, encoding='UTF-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

class Get_news(object):
    """
     获取新闻网页内容和新闻内容并将文字保存到本地
    """
    def __init__(self):
        """ 初始化该类 """

        self.html = "https://news.sina.com.cn/china/" # 新闻网址
        self.news_list = []
        self.div_list = self.getnews_herf(self.html) # 调用函数获取新闻网页中的url。
        

        url_list = []
        for i in self.div_list:
            if i == '':
                div_list.remove(i)
        for div in self.div_list[0:31]:
            url = div.xpath('./a/@href')[0]
            # print(url)
            url_list.append(url)
        # 任务列表对象。    
        tasks = [asyncio.ensure_future(self.write_news(new_url)) for new_url in url_list]
        loop =  asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(tasks)) # 挂起操作
        # loop.close()
        self.f.close()


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

    async def write_news(self,new_url):
        self.f = open('news.txt','w',encoding='utf-8')
        # print(time.time())
        # url = div.xpath('./a/@href')[0]
        async with ClientSession() as session:
            # 使用异步编程访问网页
            async with session.get(new_url) as response:
                response = await response.text(encoding='utf-8')
                # print(response)
                bs_obj = BeautifulSoup(response, 'html.parser')
                # bs_obj为网页信息
                # logger.debug(f'{bs_obj} is done')
                # 获取网站内的<p>标签内容。
                downloadList = bs_obj.select('p')
                # logger.debug(f'{downloadList}')
                # 创建一个空列表，后续存入新闻内容。
                text_list = []
                # 获取符合条件的<p>标签内容。
                text_re = re.compile(r'<p ?(cms-style="font-L")?>(\s+?\S+?)</p>')
                # print(downloadList)
                for txt in downloadList:
                    html="{}".format(txt)
                    # 比较符合条件的p标签内容
                    # print(html)
                    text_list += text_re.findall(html)
                    # print(text_list)
                # with open('news2.txt', 'a+',encoding='utf-8') as f:
                # for text_tuple in text_list:
                await self.write_file(text_list)


    async def write_file(self,text_list):
        for txt in text_list:
            # print(txt[1])
            self.f.write(txt[1])
        self.f.write('\n爬取时间：'+str((time.strftime("%Y-%m-%d %H：%M：%S", time.localtime())))+'\n')
        self.f.write('\n')

if __name__ == "__main__":
    Get_news()