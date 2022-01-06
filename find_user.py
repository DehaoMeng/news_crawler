"""
	本模块功能是登陆时链接用户数据库并查询用户账号数据.
"""

import pymysql as pm
import dispose_data as dd
import traceback
import tkinter as tk
from tkinter import messagebox
import enr as er
import Gui as g

class Enroll_database(object):
	"""
	查找登陆账户是否在数据库中
	"""
	def __init__(self,admin_name,admin_pwd,admin_window):
		"""
		初始化类，链接数据库信息，
		"""
		self.admin_name = admin_name
		self.admin_pwd = admin_pwd
		self.db = pm.connect(host='localhost', user='root', passwd='123456', port=3306)
		# 链接数据库游标
		self.cur = self.db.cursor()
		self.cur.execute("use account;")
		# 调用函数判断是否有该用户
		self.find_username(admin_window)

	def find_username(self,admin_window):
		if self.admin_name != '' and self.admin_pwd != '':
			# 按用户名查找信息
			self.cur.execute("select * from accounttable where username=%s",self.admin_name)
			try:
				self.idword = list(self.cur.fetchone())
				# 判断有无该用户名
				if self.idword != None:
					# 判断用户名与数据库中是否相同
					if self.admin_name == self.idword[1]:
						# 判断密码是否相同
						if self.admin_pwd == self.idword[2]:
							# 提示框，登陆成功
							tk.messagebox.showinfo(title='成功',message='登陆成功,可以开始爬取新闻!')
							# 登陆界面自动关闭，打开爬取界面
							admin_window.destroy()
							# 创建新窗口
							# self.root = tk.Tk()
							# self.root.title('爬取新闻数据')
							# self.root.geometry('600x500')
							# 调用Gui.py中的Gui()
							g.Gui()
							# self.root.mainloop()
						else:
							# 密码错误后，提示窗口
							tk.messagebox.showerror(message='密码错误，您无权爬取新闻。')
			# 用户名不在数据库中，提示框
			except:
				tk.messagebox.showerror(title='Error',message='请您先注册成为用户,再登陆!')
		# 输入的数据为空时
		elif self.admin_name == '' or self.admin_pwd == '':
			tk.messagebox.showerror(title='Error',message='用户名或密码不能为空')







if __name__ == "__main__":
	Enroll_database()