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
# logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level = logging.DEBUG)
log_path='log.log'
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(log_path, mode='a+', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

class Get_news(object):
    """
     获取新闻网页内容和新闻内容并将文字保存到本地
    """
    def __init__(self,url):
        """ 初始化该类 """
        # 输入新闻网页
        self.html = url # 新闻网址(需要更改)
        # self.html = "https://news.sina.com.cn/china/" # 新闻网址
        self.div_list = self.getnews_herf(self.html) # 调用函数获取新闻网页中的url的div标签。
        # 新建一个列表，存储具体的新闻url
        url_list = []
        # 循环判断列表中是否有空值
        for i in self.div_list:
            # 删除获得空值
            if i == '':
                div_list.remove(i)
        # 循环输入最新的30篇新闻url
        for div in self.div_list[0:31]:
            # xpath获得a标签中的新闻url
            url = div.xpath('./a/@href')[0]
            # 将url加入到之前创建的空列表
            url_list.append(url)
        # 任务列表对象tasks，利用循环将url_list中的每个url都进行爬取操作加入到tasks中   
        tasks = [asyncio.ensure_future(self.write_news(new_url)) for new_url in url_list]
        # 获取循环事件
        loop =  asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(tasks))
        # 关闭打开的新闻文本文档
        self.f.close()


    def getnews_herf(self,url):
        """
         获取网页中具体新闻的div标签列表
        """
        # 获得新闻网站的响应数据
        html = urllib.request.urlopen(url).read()
        html = html.decode('utf-8')
        # 获取url的div标签
        tree = etree.HTML(html)
        div_list = tree.xpath('//div[@class="left-content-1 marBot"]/div/ul/li')
        # 返回div列表
        return div_list

    async def write_news(self,new_url):
        # 打开文件
        self.f = open('news.txt','w',encoding='utf-8')
        async with ClientSession() as session:
            # 使用异步编程访问网页
            async with session.get(new_url) as response:
                # 输出日志,保存爬取网页url和时间
                logger.debug(f'{new_url} is done.')
                # 一次获取网页的响应,等待期间执行下一次响应(挂起操作)
                response = await response.text(encoding='utf-8')
                # bs_obj为网页信息
                bs_obj = BeautifulSoup(response, 'html.parser')
                # 获取网站内的<p>标签内容
                downloadList = bs_obj.select('p')
                # 创建一个空列表，后续存入新闻内容。
                text_list = []
                # 获取符合条件的<p>标签内容
                text_re = re.compile(r'<p ?(cms-style="font-L")?>(\s+?\S+?)</p>')
                # print(downloadList)
                for txt in downloadList:
                    # 所有的p标签内容依次匹配
                    html="{}".format(txt)
                    # 比较符合条件的p标签内容,将符合内容的加入到文本列表中
                    text_list += text_re.findall(html)
                # 挂起写入操作,减少响应时间
                await self.write_file(text_list)


    async def write_file(self,text_list):
        # 向文本文件内写入新闻信息
        for txt in text_list:
            self.f.write(txt[1])
        self.f.write('\n爬取时间：'+str((time.strftime("%Y-%m-%d %H：%M：%S", time.localtime())))+'\n')
        self.f.write('\n')

if __name__ == "__main__":
    Get_news()