"""
    本模块是初始登陆界面,也是主模块.
    Login_face()类是用于打开登陆窗口.
"""


import tkinter as tk
from tkinter import messagebox
import Gui as g
import enroll as el
import find_user as fu


class Login_face(object):
    """
    登陆查看词云等信息。
    """
    def __init__(self):
        admin_window = tk.Tk()
        admin_window.title("管理员登陆窗口")
        admin_window.geometry("300x200")
        admin_window.resizable(width=False, height=False)
        tk.Label(admin_window, text='用户名:').place(x=50, y=60)
        tk.Label(admin_window, text='密码:').place(x=50, y=100)
        # 用户名输入框
        entry_usr_name = tk.Entry(admin_window)
        entry_usr_name.place(x=110, y=60)
        # 密码输入框 
        entry_usr_pwd = tk.Entry(admin_window, show='*')
        entry_usr_pwd.place(x=110, y=100)

        def get_user():
            admin_name = str(entry_usr_name.get())
            admin_pwd = str(entry_usr_pwd.get())
            # print(admin_name,admin_pwd)
            fu.Enroll_database(admin_name,admin_pwd,admin_window)

        bt_login = tk.Button(admin_window, text='登录', command=get_user)
        bt_login.place(x=80, y=140)
        bt_enroll = tk.Button(admin_window,text='注册',command=el.Enroll)
        bt_enroll.place(x=150,y=140)
        bt_logquit = tk.Button(admin_window, text='退出', command=admin_window.destroy)
        bt_logquit.place(x=220, y=140)
        admin_window.mainloop()

if __name__ == "__main__":
    Login_face()