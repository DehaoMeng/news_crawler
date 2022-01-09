"""
	本模块是爬虫图形界面
	Gui()是用于实现配置图形化界面
"""
import time
import pickle
import threading
import tkinter as tk
import dispose_data as dd
import Get as gt
from tkinter import messagebox
from PIL import ImageTk, Image
import database as db
import Login as lg
import tkinter.ttk
from tkinter import ttk
import progressbar


class Gui(object):
	"""
	创建初始化界面
	"""
	def __init__(self):
		self.window = tk.Tk()
		self.window.title('爬取新闻数据')
		self.window.geometry('600x500')
		self.window.resizable(width=False, height=False)
		self.window.config()
		self.recommand = tk.Frame(self.window,width=600,height=500,bg='pink')
		self.recommand.pack()
		self.recommand.place(x=0,y=0)
		# 设置按钮调用爬虫函数。
		tk.Label(self.recommand,text='主菜单',font=('heiti',25),width=20,height=1,bg='pink').place(relx=0.24,rely=0.1)
		tk.Label(self.recommand,text='请输入需要爬取的新闻网址',font=('heiti',20),width=30,height=1,bg='pink').place(relx=0.17,rely=0.2)
		self.t = tk.Entry(self.recommand,width=35,font=('heiti',15))
		self.t.place(relx=0.24,rely=0.26,height=40)
		tk.Button(self.recommand, text="开始爬取数据", font=('heiti', 25), width=20, height=1, relief='groove', bg='pink', command=self.second_face).place(relx=0.24,rely=0.35)
		tk.Button(self.recommand,text='退出登陆',font=('heiti',25),width=20,height=1,relief='groove', bg='pink', command=self.exit0).place(relx=0.24,rely=0.55)
		tk.Button(self.recommand,text='帮助文档',font=('heiti',25),width=20,height=1,relief='groove', bg='pink', command=self.helpuse).place(relx=0.24,rely=0.75)
		tk.Label(self.recommand,text="By孟德昊",font=('heiti',15),width=20,height=1,bg='pink').place(relx=0.76,rely=0.95)
		

	def helpuse(self):
		"""
		打开新窗口帮助文件获取需要输入的新闻网址
		"""
		root = tk.Tk()
		root.geometry('400x300')
		with open('help.txt','r',encoding='utf-8') as f:
			txt = f.read()
		tk.Label(root,text=txt,font=('heiti',15),width=100,wraplength=2000).place(relx=-0.75,rely=0.4)
		root.mainloop()

	def exit0(self):
		# 退出登陆界面
		self.window.destroy()
		lg.Login_face()

	def second_face(self):
		"""
		正在爬取
		"""
		# 毁坏
		url = self.t.get()
		if not url:
			tk.messagebox.showerror(title='Error',message='请输入正确网址')
		else:
			self.recommand.destroy()
			self.recommand1 = tk.Frame(self.window,width=600,height=500,bg='pink')
			self.recommand1.pack()
			self.recommand1.place(x=0,y=0)
			tk.Label(self.recommand1,text='正在爬取数据',font=('heiti',15),width=20,height=1,bg='pink').place(relx=0.3,rely=0.45)
			self.p1 = tk.ttk.Progressbar(self.recommand1, length=200,mode="indeterminate",orient=tk.HORIZONTAL)
			self.p1.place(relx=0.3,rely=0.5)
			self.p1.start()
			tk.messagebox.showinfo(title='display_messagebox',message='正在爬取')
			gt.Get_news(url)
			self.third_face()

	def third_face(self):
		"""
		爬取完成界面
		"""
		self.recommand1.destroy()
		self.display_messagebox()
		self.windows2 = tk.Frame(self.window,width=800,height=840,bg='pink')
		self.windows2.place(x=0,y=0)
		tk.Label(self.windows2,text='爬取完成',font=('heiti',15),width=20,height=1,bg='pink').place(relx=0.24,rely=0.02)
		scroll = tk.Scrollbar(bg='pink')
		text = tk.Text(self.windows2,width=70,height=20,bg='pink')
		text.config(state='normal')
		scroll.config(command=text.yview)
		text.config(yscrollcommand=scroll.set)
		text.place(x=50,y=50)
		with open('news.txt','r',encoding='utf-8') as fp:
			txt = fp.read()
		text.insert('end',txt)
		scroll.pack(anchor='ne',fill='y',expand=True)
		tk.Button(self.windows2,text='写入数据库',font=('heiti', 15), width=20, height=1, relief='groove', bg='pink', command=self.write_daba).place(relx=0.24,rely=0.4)
		tk.Button(self.windows2, text='写入excel表', font=('heiti', 15), width=20, height=1, relief='groove', bg='pink', command=self.writing_excel).place(relx=0.24, rely=0.45)
		tk.Button(self.windows2,text='查看数据分析',font=('heiti', 15), width=20, height=1, relief='groove', bg='pink', command=self.zhuxingtu).place(relx=0.24,rely=0.5)
		tk.Button(self.windows2, text='查看词云', font=('heiti', 15), width=20, height=1, relief='groove', bg='pink', command=self.ciyun).place(relx=0.24, rely=0.55)
		tk.Button(self.windows2, text='返回上一级', font=('heiti', 15), width=10, height=5, relief='groove', bg='pink', command=self.back).place(relx=0.54, rely=0.40)

	
	def back(self):
		"""
		退回主操作界面
		"""
		self.window.destroy()
		Gui()
		self.window.mainloop()
		
	def writing_excel(self):
		"""
		获取到的内容分析写入excel表
		"""
		dd.Write_excel()

	def write_daba(self):
		"""
		当点击查看数据分析时，数据写入数据库
		"""
		db.Database_connect()

	def zhuxingtu(self):
		"""
		当点击查看数据分析时，调用登陆信息查询柱状图
		"""
		dd.Matp()


	def ciyun(self):
		"""
		当点击查看词云按钮时，调用登陆信息查询词云图

		"""
		dd.Dispose()
		



	def display_messagebox(self):
		return messagebox.showinfo(title='display_messagebox',message='爬取完成')
		self.p1.stop()
		self.recommand1.destroy()



if __name__ == "__main__":
	Gui()
