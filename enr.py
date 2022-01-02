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
		self.ifexist_database()
		self.cur.execute("use account;")
		self.ifexist_datatable()
		self.find_username()
		self.cur.close()
		self.db.close

	def write_table(self):
		try:
			self.cur.execute("insert into accounttable(username,passwd) values (%s,%s)",(self.admin_name,self.admin_pwd))
			self.db.commit()
			# print("已写入")
		except:
			traceback.print_exc()
			self.db.rollback()

	def ifexist_database(self):
		self.cur.execute("show databases;")
		self.database_data = self.cur.fetchall()
		self.listdata_base = list(self.database_data)
		# print(self.listdata_base)
		if ('account',) in self.listdata_base:
			# print("数据库已存在，无需创建")
			# tk.messagebox.showerror(title='提示',
			# 	message='数据库已存在，无需创建')
			return 0
		else:
			# print("数据库不存在，正在创建")
			self.cur.execute("create database account;")
			tk.messagebox.showerror(title='提示',
				message='数据库不存在，正在创建')
			return 0

	def ifexist_datatable(self):
		self.cur.execute("show tables;")
		self.table_data  = self.cur.fetchall()
		self.listdata_table = list(self.table_data)
		# print(self.listdata_table)
		if ('accounttable',) in self.listdata_table:
			# tk.messagebox.showerror(title='提示',
			# 	message='数据表已存在，无需创建')
			return 0
		else:
			# print("数据表不存在，正在创建")
			tk.messagebox.showerror(title='提示',
				message='数据库不存在，正在创建')
			self.cur.execute("create table accounttable(id int(4) AUTO_INCREMENT,username Varchar(8) PRIMARY KEY,passwd varchar(10));")

	def find_username(self):
		if self.cur.execute("select * from accounttable where username=%s;",self.admin_name):
			tk.messagebox.showerror(title='Error',message='该用户已存在,无需创建!')
		else:
			self.write_table()
			tk.messagebox.showinfo(title='成功',message='注册成功,请登录!')


if __name__ == "__main__":
	Enroll_database()