"""
	本模块功能是链接数据库并写入数据
"""

import pymysql as pm
import dispose_data as dd
import traceback
import tkinter as tk
from tkinter import messagebox

class Database_connect(object):
	"""
	链接数据库(或新建数据库)
	"""
	def __init__(self):
		self.db = pm.connect(host='localhost', user='root', passwd='123456', port=3306)
		self.cur = self.db.cursor()
		self.ifexist_database()
		self.cur.execute("use wordstorage;")
		self.ifexist_datatable()
		with open('news.txt','r',encoding='utf-8') as f:
			data = f.read()
		self.word_counts_top100=dict(dd.Dispose.dispose(self, data))
		self.write_table()
		self.cur.close()
		self.db.close

	def write_table(self):
		n = 1
		for k,v in self.word_counts_top100.items():
			# print(n,k,v,"已写入")
			# print("已经写入")
			try:
				self.cur.execute("insert into worddata(id,word,frequency) values (%s,%s,%s)",(str(n),k,v))
				self.db.commit()
				# print("已写入")
				n += 1
			except:
				traceback.print_exc()
				self.db.rollback()
		tk.messagebox.showinfo(title='提示',message='已经全部写入')

	def ifexist_database(self):
		self.cur.execute("show databases;")
		self.database_data = self.cur.fetchall()
		self.listdata_base = list(self.database_data)
		# print(self.listdata_base)
		if ('wordstorage',) in self.listdata_base:
			# print("数据库已存在，无需创建")
			# tk.messagebox.showerror(title='提示',
			# 	message='数据库已存在，无需创建')
			return 0
		else:
			print("数据库不存在，正在创建")
			self.cur.execute("create database wordstorage;")
			tk.messagebox.showerror(title='提示',
				message='数据库不存在，正在创建')
			return 0

	def ifexist_datatable(self):
		self.cur.execute("show tables;")
		self.table_data  = self.cur.fetchall()
		self.listdata_table = list(self.table_data)
		# print(self.listdata_table)
		if ('worddata',) in self.listdata_table:
			self.cur.execute("select * from worddata;")
			if self.cur.fetchall() != None:
				tk.messagebox.showerror(title='提示',
					message='数据表有内容，已完成清除')
				# print("已清除")
				self.cur.execute("truncate worddata;")
			# print("数据表已存在，无需创建")
			# tk.messagebox.showerror(title='提示',
			# 	message='数据表已存在，无需创建')
			return 0
		else:
			# print("数据表不存在，正在创建")
			tk.messagebox.showerror(title='提示',
				message='数据库不存在，正在创建')
			self.cur.execute("create table worddata;")




if __name__ == "__main__":
	Database_connect()