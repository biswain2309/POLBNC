from tkinter import *
from os import path
import shutil,os


def copy_src(inp_path):
    print('path to check :', inp_path)
    if path.exists(inp_path):
        src = path.realpath(inp_path)
        head,tail = path.split(src)
        path_dst = "D:\OSS\POLBNC"
        dst = path_dst + tail
        print('dest path :', dst)
        shutil.copy(src, dst)

master = Tk()
Label(master, text='Enter path of POL file').grid(row=0)
Label(master, text='Enter path of BIL file').grid(row=1)
Label(master, text='Enter path of POLBNC file').grid(row=2)
e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
user_inp1 = e1.get()
user_inp2 = e2.get()
user_inp3 = e3.get()

copy_src(user_inp1)
copy_src(user_inp2)
copy_src(user_inp3)

mainloop()

