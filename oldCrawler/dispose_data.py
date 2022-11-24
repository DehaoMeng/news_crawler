"""
    本模块内容功能是处理文字数据保存生成词云以及柱形图。
    Dispose_data()类是处理文字信息，获取出现频率最高的一百个次，生词中国地图样式的词云。
    Matp()类是生成出现频率最高的20个词，生成柱形图。
"""

import re
import jieba
import collections
from tkinter import messagebox
import tkinter as tk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image,ImageSequence
import numpy as np
from os import environ
environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
environ["QT_SCREEN_SCALE_FACTORS"] = "1"
environ["QT_SCALE_FACTOR"] = "1"
jieba.setLogLevel(jieba.logging.INFO)
import xlwt


class Dispose(object):
    """
    处理数据并生成词云
    """
    def __init__(self):
        """ 初始化处理数据类 """
        with open('news.txt','r',encoding='utf-8') as f:
            data = f.read()
        self.word_counts_top100=dict(self.dispose(data))
        self.create_word_cloud()

    def dispose(self,data):
        """
         文本预处理  去除一些无用的字符   只提取出中文出来
         """
        self.new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
        self.new_data = " ".join(self.new_data)
        # 文本分词
        self.seg_list_exact = jieba.cut(self.new_data, cut_all=True)
        self.result_list = []
        for word in self.seg_list_exact:
            # 设置停用词并去除单个词
            if len(word) > 1:
                self.result_list.append(word)

        # 筛选后统计
        word_counts = collections.Counter(self.result_list)
        # 获取前100最高频的词
        word_counts_top100 = word_counts.most_common(100)
        return word_counts_top100

    def create_word_cloud(self):
        """ 打开词云 """
        image= Image.open('ditu.png')#打开背景图
        graph = np.array(image)#读取背景图
        # 绘制词云
        my_cloud = WordCloud(
            background_color='white',  # 设置背景颜色  默认是black
            width=900, height=600,
            max_words=101,            # 词云显示的最大词语数量
            font_path='simhei.ttf',   # 设置字体  显示中文
            max_font_size=800,         # 设置字体最大值
            min_font_size=10,         # 设置子图最小值
            random_state=50,          # 设置随机生成状态，即多少种配色方案
            mask=graph                # 设置背景模板
        ).generate_from_frequencies(self.word_counts_top100)

        # 显示生成的词云图片 
        plt.imshow(my_cloud, interpolation='bilinear')
        # 显示设置词云图中无坐标轴
        plt.axis('off')
        plt.show()
        my_cloud.to_file('3.png')

class Matp(object):
    """
    本类用于生成数据保存的柱形图。
    """
    def __init__(self):
        """
        初始化柱形图类
        """
        # 读取文件内容
        with open('news.txt','r',encoding='utf-8') as f:
            data = f.read()
        # 调用之前统计的最高频的100词函数获取词以及词出现的次数。
        self.word_counts_top100=dict(Dispose.dispose(self,	data))
        # 生成柱形图
        self.pic_creat()

    def pic_creat(self):
        """
        生成最高频20个词的柱形图函数
        """
        # 获取横纵坐标
        x = list(self.word_counts_top100.keys())[0:20]
        y = list(self.word_counts_top100.values())[0:20]
        # 创建柱形图
        fig, axes = plt.subplots(ncols=1, figsize=plt.figaspect(1./2))
        axes.set_xlabel('出现词')
        axes.set_ylabel('出现次数')
        axes.set_title('十篇新文中最高频率出现的20个词')
        # 在柱形图上显示具体次数
        for a, b in zip(x, y):
            plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=11)
        # 设置字体，否则无法显示中文
        plt.rcParams['font.sans-serif']=['SimHei']
        vert_bars = axes.bar(x, y, color='lightblue', align='center')
        plt.show()

class Write_excel(object):
    def __init__(self):
        with open('news.txt','r',encoding='utf-8') as f:
            data = f.read()
        self.word_counts_top100 = dict(Dispose.dispose(self,data))
        self.write_excel()

    def set_style(self,name,height,bold=False):
        # 初始化样式
        style = xlwt.XFStyle()
        # 创建字体样式
        font = xlwt.Font()
        # 设置字体
        font.name = name
        # 无黑体
        font.bold = bold
        # 字体颜色
        font.color_index = 0
        # 行高
        font.height = height
        style.font = font
        return style
    def write_excel(self):
        # 新建一个excel工作表单
        self.fp = xlwt.Workbook()
        sheet1 = self.fp.add_sheet('统计',cell_overwrite_ok=True)
        # 设置要输入的第一行的内容
        row0 = ["单词","频数"]
        # 设置输入的列内容
        colum0 = [k for k in self.word_counts_top100.keys()]
        colum1 = [v for v in self.word_counts_top100.values()]
        #写第一行
        for i in range(0,len(row0)):
            sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))
        #写第一列
        for i in range(0,len(colum0)):
            sheet1.write(i+1,0,colum0[i],self.set_style('Times New Roman',220,True))
        # 写第二列
        for i in range(0,len(colum1)):
            sheet1.write(i+1,1,colum1[i],self.set_style('Times New Roman',220,True))

        self.fp.save('result.xls')
        tk.messagebox.showinfo(title='提示',message='已经全部写入excel文件')

if __name__ == "__main__":
    # Get_news()
    Dispose()
    # Matp()
    # Write_excel()