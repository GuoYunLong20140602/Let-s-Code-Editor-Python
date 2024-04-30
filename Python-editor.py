import time
import tkinter as tk  # 导入Tkinter
import tkinter.ttk as ttk  # 导入Tkinter.ttk
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText  # 导入ScrolledText

import pyperclip as pc

title = "Let's Code-Editor-Python"

count = 0
# 建立主窗口
root = tk.Tk()
root.title(title)
root.geometry("800x800+0+0")

# 放几个按钮
frame = tk.Frame(root)
new_file_button = tk.Button(frame, text="新文件", font=("宋体", 20))
read_file_button = tk.Button(frame, text="读取文件", font=("宋体", 20))
to_save_file_button = tk.Button(frame, text="另存文件", font=("宋体", 20))
runpy_button = tk.Button(frame, text="执行程序", font=("宋体", 20))
clear_messages_button = tk.Button(frame, text="清空信息窗", font=("宋体", 20))

new_file_button.pack(side=tk.LEFT)
read_file_button.pack(side=tk.LEFT)
to_save_file_button.pack(side=tk.LEFT)
runpy_button.pack(side=tk.LEFT)
clear_messages_button.pack(side=tk.RIGHT)
frame.pack(side=tk.TOP, fill=tk.BOTH)

# 放置一个文本框
global edit_box
edit_box = ScrolledText(bg="white", font=("Monaco", 14))
edit_box.pack(fill=tk.BOTH, expand=1)
edit_box.focus_set()

global filename
filename = "Unnamed.py"

# 实现按钮功能
def new_file():  # 新文件
    global edit_box, filename
    edit_box.delete(1.0, tk.END)
    filename = "Unnamed.py"


def read_file():  # 读取文件
    global edit_box, filename
    filename2 = askopenfilename(defaultextension=".py")
    if filename2 != "":
        with open(filename2, "r", encoding="utf-8", errors="ignore") as f:
            edit_box.delete(1.0, tk.END)  # delete all
            edit_box.insert(1.0, f.read())
            filename = filename2


def to_save_file():  # 另存文件
    global edit_box, filename
    filename = asksaveasfilename(initialfile=filename, defaultextension=".py")
    if filename != "":
        with open(filename, "w", encoding="utf-8") as fh:
            msg = edit_box.get(1.0, tk.END)
            fh.write(msg)


# 为按钮设置功能
new_file_button["command"] = lambda: new_file()
read_file_button["command"] = lambda: read_file()
to_save_file_button["command"] = lambda: to_save_file()

##为信息框设置一个容器
frame2 = tk.LabelFrame(root, text="信息框", height=100)
frame2.pack(fill=tk.BOTH, expand=1)

global textMess

# 放置一个文本框作为信息输出窗口
textMess = ScrolledText(frame2, bg="white", height=100, font=("宋体", 17))
textMess.pack(fill=tk.BOTH, expand=1)
##清空信息窗
def clearMess():
    global textMess
    textMess.delete(1.0, tk.END)


# 用户输出信息
def my_print(txt):
    global textMess
    if textMess != None:
        textMess.insert(tk.END, txt)
        textMess.see(tk.END)


# 输出彩色信息
def color_print(txt, color="black"):
    global textMess
    if textMess != None:
        if color != "black":
            textMess.tag_config(color, foreground=color)
        textMess.insert(tk.END, txt, color)
        textMess.see(tk.END)


# 运行python文件
def runpy():
    global edit_box, textMess, count
    count += 1
    try:
        msg = edit_box.get(1.0, tk.END)
        mg = globals()
        ml = locals()
        print(f'第{count}次运行, {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        exec(msg, mg, ml)
    except Exception as e:
        color_print("\n#用户代码出错:" + str(e) + "\n", "red")
        messagebox.showerror("错误", f"报错了!报错信息:\n {str(e)}")


class Commands:
    def __init__(self, box):
        self.box = box

    def copy_line(self):
        line_index = self.box.index(tk.INSERT).split(".")[0]
        line_data = self.box.get(line_index + ".0", "end")
        pc.copy(line_data)

    def cut_line(self):
        line_index = self.box.index(tk.INSERT).split(".")[0]
        line_data = self.box.get(line_index + ".0", "end")
        pc.copy(line_data)
        self.box.delete(line_index + ".0", "end")

    def paste(self):
        text = pc.paste()
        self.box.insert(tk.INSERT, text)


runpy_button["command"] = lambda: runpy()
clear_messages_button["command"] = lambda: clearMess()

# 菜单栏
menu_bar = tk.Menu(root, tearoff=0)

commands = Commands(edit_box)
edit_box.bind("<Control-c>", lambda event: commands.copy_line())
edit_box.bind("<Control-x>", lambda event: commands.cut_line())
edit_box.bind("<Control-v>", lambda event: commands.paste())
edit_box.bind("<Control-b>", lambda event: runpy())
edit_box.bind("<Control-r>", lambda event: clearMess())
edit_box.bind("<Control-s>", lambda event: to_save_file())
edit_box.bind("<Control-o>", lambda event: read_file())
edit_box.bind("<Control-n>", lambda event: new_file())
edit_box.bind("<Control-q>", lambda event: root.quit())

# 文件栏
file_bar = tk.Menu(menu_bar, tearoff=0)
file_bar.add_command(label="新建", command=new_file)
file_bar.add_command(label="打开", command=read_file)
file_bar.add_command(label="另保存", command=to_save_file)
file_bar.add_separator()
file_bar.add_command(label="退出", command=root.quit)

menu_bar.add_cascade(label="文件", menu=file_bar)
# 编辑栏
edit_bar = tk.Menu(menu_bar, tearoff=0)
edit_bar.add_command(label="复制行", command=lambda: commands.copy_line())
edit_bar.add_command(label="剪切行", command=lambda: commands.cut_line())
edit_bar.add_command(label="粘贴", command=lambda: commands.paste())

menu_bar.add_cascade(label="编辑", menu=edit_bar)

root.config(menu=menu_bar)
# 运行主循环
root.mainloop()
