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
	def __init__(self,master):
		self.window = master
		self.window.config()
		self.recommand = tk.Frame(self.window,width=600,height=500)
		self.recommand.pack()
		self.recommand.place(x=0,y=0)
		# 设置按钮调用爬虫函数。
		tk.Label(self.recommand,text='主菜单',font=('heiti',25),width=20,height=1).place(relx=0.24,rely=0.2)
		b = tk.Button(self.recommand, text="开始爬取数据", font=('heiti', 25), width=20, height=1,command=self.dele_initmenu)
		b.place(relx=0.24,rely=0.35)
		tk.Button(self.recommand,text='退出登陆',font=('heiti',25),width=20,height=1,command=self.exit0).place(relx=0.24,rely=0.55)
		tk.Button(self.recommand,text='帮助文档',font=('heiti',25),width=20,height=1,command=self.helpuse).place(relx=0.24,rely=0.75)
		tk.Label(self.recommand,text="By孟德昊",font=('heiti',15),width=20,height=1).place(relx=0.76,rely=0.95)

	def helpuse(self):
		root = tk.Tk()
		root.geometry('400x300')
		with open('help.txt','r',encoding='utf-8') as f:
			txt = f.read()
		tk.Label(root,text=txt,font=('heiti',15),width=100,wraplength=200).place(relx=-0.75,rely=0.4)
		root.mainloop()

	def exit0(self):
		self.window.destroy()
		lg.Login_face()


	def dele_initmenu(self):
		self.recommand.destroy()
		self.new_menu()

	def new_menu(self):
		"""
		正在爬取
		"""
		self.recommand1 = tk.Frame(self.window,width=600,height=500)
		self.recommand1.pack()
		self.recommand1.place(x=0,y=0)
		tk.Label(self.recommand1,text='正在爬取数据',font=('heiti',15),width=20,height=1).place(relx=0.3,rely=0.45)
		self.p1 = tk.ttk.Progressbar(self.recommand1, length=200,mode="indeterminate",orient=tk.HORIZONTAL)
		self.p1.place(relx=0.3,rely=0.5)
		self.p1.start()
		tk.messagebox.showinfo(title='display_messagebox',
							   message='正在爬取')
		# self.thread_it(gt.Get_news)
		gt.Get_news()
		self.second_menu()

	def second_menu(self):
		"""
		爬取完成界面
		"""
		# time.sleep(6)
		# self.p1.stop()
		self.display_messagebox()
		self.windows2 = tk.Frame(self.window,width=800,height=840)
		self.windows2.place(x=0,y=0)
		tk.Label(self.windows2,text='爬取完成',font=('heiti',15),width=20,height=1).place(relx=0.24,rely=0.3)
		tk.Button(self.windows2,text='写入数据库',font=('heiti', 15), width=20, height=1, command=self.write_daba).place(relx=0.24,rely=0.4)
		tk.Button(self.windows2,text='查看数据分析',font=('heiti', 15), width=20, height=1, command=self.zhuxingtu).place(relx=0.24,rely=0.45)
		tk.Button(self.windows2, text='查看词云', font=('heiti', 15), width=20, height=1,command=self.ciyun).place(relx=0.24, rely=0.5)
		

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

	def thread_it(self, func):
		"""
		启动多线程
		"""
		t1 = threading.Thread(target=func)
		# t2 = threading.Thread(target=self.p1.start)
		# t.setDaemon(True)
		t1.start()
		# t2.start()
		t1.join()


if __name__ == "__main__":
	root = tk.Tk()
	root.geometry('600x500')
	Gui(root)
	root.mainloop()