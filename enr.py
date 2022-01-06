"""
	本模块功能是注册时链接用户数据库并写入用户账号数据.
"""

import pymysql as pm
import dispose_data as dd
import traceback
import tkinter as tk
from tkinter import messagebox

class Enroll_database(object):
	"""
	链接用户数据库(或新建用户数据库)
	"""
	def __init__(self,admin_name,admin_pwd):
		self.admin_name=admin_name
		self.admin_pwd=admin_pwd
		self.db = pm.connect(host='localhost', user='root', passwd='123456', port=3306)
		self.cur = self.db.cursor()
		# 判断用户信息数据库是否存在,不存在则创建库
		self.ifexist_database()
		# 使用该数据库
		self.cur.execute("use account;")
		# 判断数据表是否存在
		self.ifexist_datatable()
		# 判断用户是否存在
		self.find_username()
		# 断开游标和数据库的链接
		self.cur.close()
		self.db.close

	def write_table(self):
		# 向数据库中写入用户信息
		try:
			self.cur.execute("insert into accounttable(username,passwd) values (%s,%s)",(self.admin_name,self.admin_pwd))
			self.db.commit()
		except:
			# 写入失败则进行回滚操作
			traceback.print_exc()
			self.db.rollback()

	def ifexist_database(self):
		# 判断是否存在数据库
		self.cur.execute("show databases;")
		self.database_data = self.cur.fetchall()
		self.listdata_base = list(self.database_data)
		if ('account',) in self.listdata_base:
			return 0
		else:
			self.cur.execute("create database account;")
			tk.messagebox.showerror(title='提示',
				message='数据库不存在，正在创建')
			return 0

	def ifexist_datatable(self):
		# 判断数据表是否存在
		self.cur.execute("show tables;")
		self.table_data  = self.cur.fetchall()
		self.listdata_table = list(self.table_data)
		if ('accounttable',) in self.listdata_table:
			return 0
		else:
			tk.messagebox.showerror(title='提示',
				message='数据表不存在，正在创建')
			self.cur.execute("create table accounttable(id int(4) AUTO_INCREMENT,username Varchar(8) PRIMARY KEY,passwd varchar(10));")

	def find_username(self):
		# 向数据表内查找是否存在该用户了
		if self.cur.execute("select * from accounttable where username=%s;",self.admin_name):
			tk.messagebox.showerror(title='Error',message='该用户已存在,无需创建!')
		else:
			self.write_table()
			tk.messagebox.showinfo(title='成功',message='注册成功,请登录!')


if __name__ == "__main__":
	Enroll_database()