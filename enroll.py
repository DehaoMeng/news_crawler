"""
	本模块用来完成用户注册功能.
	Enroll()类是用户注册界面.
"""

import tkinter as tk
from tkinter import messagebox
import pymysql as pm
import re
import enr as er

class Enroll(object):
    def __init__(self):
        # 新建用户注册界面
        self.root = tk.Tk()
        self.root.title('用户注册')
        self.root.geometry("300x200")
        self.root.resizable(width=False, height=False)
        tk.Label(self.root, text='用户名:').place(x=50, y=60)
        tk.Label(self.root, text='密码:').place(x=50, y=100)
        # 用户名输入框
        self.entry_usr_name = tk.Entry(self.root)
        self.entry_usr_name.place(x=110, y=60)
        tk.Label(self.root,text='请输入一个5-8位的用户名(英文或数字组合)',font=('heiti',8)).place(x=60,y=83)
        # 密码输入框
        self.entry_usr_pwd = tk.Entry(self.root, show='*',textvariable='请输入一个5-10位的密码(英文或数字组合)')
        self.entry_usr_pwd.place(x=110, y=100)
        tk.Label(self.root,text='请输入一个5-10位的密码(英文或数字组合)',font=('heiti',8)).place(x=60,y=125)
        # self.entry_usr_pwd.set("请输入一个5-10位的密码(英文或数字组合)")
        tk.Button(self.root,text="注册",command=self.matching).place(x=150,y=140)
        self.root.mainloop()

    def matching(self):
        self.admin_name = self.entry_usr_name.get()
        self.admin_pwd = self.entry_usr_pwd.get()
        # 判断用户名和密码是否符合规定
        if re.match('(\\w){5,8}',self.admin_name) and re.match('(\\w){5,10}',self.admin_pwd):
            # 调用enr.py中的Enroll_database()
            er.Enroll_database(self.admin_name,self.admin_pwd)
            self.root.destroy()
        elif re.match('(\\w){5,8}',self.admin_name) == None:
            tk.messagebox.showerror(title='Error',
                message='用户名不符合输入,请重新输入!')
        elif re.match('(\\w){5,10}',self.admin_pwd) == None:
            tk.messagebox.showerror(title='Error',
                message='密码不符合输入,请重新输入!')


if __name__ == "__main__":
	Enroll()