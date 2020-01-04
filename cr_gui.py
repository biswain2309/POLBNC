import tkinter as tk
# from tkinter import simpledialog
from os import path
import pathlib
import os
import shutil
from functools import partial
import allcomp as ac
import txt_to_xcl as t


def copy_src(var_lst):
    for item in var_lst:
        inp_path = item.get()
        # inp_path = str(self.e1.get())
        head1,tail1 = path.split(inp_path)
        print('path to pass :', inp_path)
        # if path.exists(head1):
        src = path.realpath(inp_path)
        # src = pathlib.PurePath(inp_path)
        print('Source path :', src)
        # head,tail = path.split(src)
        path_dst = "/OSS/POLBNC"
        dst = path.realpath(path_dst)
        print('dest path :', dst)
        print("Source file path :", src)
        shutil.copy(src, dst)
        # os.rename()
    t.txt_excel()
    ac.col_rename(t.str_bil, t.index_col_bil)
    dfdiff_r = ac.excel_cmp(t.cols_pbc, ac.cols_bil, t.dfbil, t.dfdf, t.dfpbc)

    ac.col_rename(t.str_pol, t.index_col_pol)
    dfdiff_r = ac.excel_cmp(t.cols_pbc, ac.cols_pol, t.dfpol, dfdiff_r, t.dfpbc)

    ac.only_cells_with_red_text(dfdiff_r)


root = tk.Tk()

# root.withdraw()

# the input dialog
# user_inp1 = simpledialog.askstring(title="Test",
#                                    prompt="Enter location of POL file:")

var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()

label1 = tk.Label(root,
                     text="Enter location of POL file:").grid(row=0)
label2 = tk.Label(root,
                     text="Enter location of BIL file:").grid(row=1)
label3 = tk.Label(root,
                      text="Enter location of POLBNC file:").grid(row=2)

e1 = tk.Entry(root, textvariable = var1)
e2 = tk.Entry(root, textvariable = var2)
e3 = tk.Entry(root, textvariable = var3)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

copy_src = partial(copy_src, [var1, var2, var3])

button = tk.Button(root, text = "Submit", command=copy_src).grid(row=3)
# os.system('allcomp.py')
root.mainloop()




