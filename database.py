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
		# 判断是否存在数据库
		self.ifexist_database()
		self.cur.execute("use wordstorage;")
		# 判断是否存在数据表
		self.ifexist_datatable()
		# 打开文本文档
		with open('news.txt','r',encoding='utf-8') as f:
			data = f.read()
		# 调用dispose_data.py中获取出现的词和字数,并存储到字典中
		self.word_counts_top100=dict(dd.Dispose.dispose(self, data))
		self.write_table()
		self.cur.close()
		self.db.close

	def write_table(self):
		# 将前100高频词汇写入数据表
		n = 1
		for k,v in self.word_counts_top100.items():
			try:
				# 写入操作
				self.cur.execute("insert into worddata(id,word,frequency) values (%s,%s,%s)",(str(n),k,v))
				self.db.commit()
				n += 1
			except:
				# 写入失败,回滚操作
				traceback.print_exc()
				self.db.rollback()
		tk.messagebox.showinfo(title='提示',message='已经全部写入')

	def ifexist_database(self):
		# 判断数据库是否存在
		self.cur.execute("show databases;")
		self.database_data = self.cur.fetchall()
		self.listdata_base = list(self.database_data)
		if ('wordstorage',) in self.listdata_base:
			return 0
		else:
			self.cur.execute("create database wordstorage;")
			tk.messagebox.showerror(title='提示',
				message='数据库不存在，正在创建')
			return 0

	def ifexist_datatable(self):
		# 判断数据表是否存在
		self.cur.execute("show tables;")
		self.table_data  = self.cur.fetchall()
		self.listdata_table = list(self.table_data)
		if ('worddata',) in self.listdata_table:
			self.cur.execute("select * from worddata;")
			if self.cur.fetchall() != None:
				tk.messagebox.showerror(title='提示',
					message='数据表有内容，已完成清除')
				self.cur.execute("truncate worddata;")
			return 0
		else:
			tk.messagebox.showerror(title='提示',
				message='数据库不存在，正在创建')
			self.cur.execute("create table worddata(id varchar(4),word varchar(10),frequency varchar(10));")


if __name__ == "__main__":
	Database_connect()