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
		self.admin_name = admin_name
		self.admin_pwd = admin_pwd
		# print(self.admin_name,self.admin_pwd)
		self.db = pm.connect(host='localhost', user='root', passwd='123456', port=3306)
		self.cur = self.db.cursor()
		self.cur.execute("use account;")
		self.find_username(admin_window)

	def find_username(self,admin_window):
		if self.admin_name != '' and self.admin_pwd != '':
			self.cur.execute("select * from accounttable where username=%s",self.admin_name)
			# print(self.cur.execute("select * from accounttable where username=%s",self.admin_name))
			self.idword = list(self.cur.fetchone())
			if self.idword != None:
				if self.admin_name == self.idword[1]:
					if self.admin_pwd == self.idword[2]:
						tk.messagebox.showinfo(title='成功',message='登陆成功,可以开始爬取新闻!')
						admin_window.destroy()
						self.root = tk.Tk()
						self.root.title('爬取新闻数据')
						self.root.geometry('600x500')
						g.Gui(self.root)
						self.root.mainloop()
					else:
						tk.messagebox.showerror(message='密码错误，您无权爬取新闻。')
				elif self.cur.fetchone() == None:
					tk.messagebox.showerror(title='Error',message='请您先注册成为用户,再登陆!')
			else:
				tk.messagebox.showerror(title='Error',message='请先注册成为用户,再登陆!')
		elif self.admin_name == '' or self.admin_pwd == '':
			tk.messagebox.showerror(title='Error',message='用户名或密码不能为空')






if __name__ == "__main__":
	Enroll_database()