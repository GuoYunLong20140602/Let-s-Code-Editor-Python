import base64
import json
import threading
import time
import tkinter as tk  # 导入Tkinter
import tkinter.ttk as ttk  # 导入Tkinter.ttk
from tkinter import messagebox

# 颜色
from tkinter.colorchooser import askcolor
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText  # 导入ScrolledText

import easygui
import requests

title = "Let's Code-Editor-Python"

count = 0
# 建立主窗口
root = tk.Tk()
root.title(title)
root.geometry("800x800+0+0")

# 放几个按钮
frame = tk.Frame(root)
new_file_button = tk.Button(
    frame, text="新文件", font=("微软雅黑", 15)
)
read_file_button = tk.Button(
    frame, text="读取文件", font=("微软雅黑", 15)
)
to_save_file_button = tk.Button(
    frame, text="另存文件", font=("微软雅黑", 15)
)
runpy_button = tk.Button(frame, text="执行程序", font=("微软雅黑", 15))


new_file_button.pack(side=tk.LEFT)
read_file_button.pack(side=tk.LEFT)
to_save_file_button.pack(side=tk.LEFT)
runpy_button.pack(side=tk.LEFT)

frame.pack(side=tk.TOP, fill=tk.BOTH)

global edit_box
# 放置一个文本框
edit_box = ScrolledText(bg="white", font=("Monaco", 20))
edit_box.pack(fill=tk.BOTH, expand=1)
edit_box.focus_set()

global filename
filename = "Unnamed.py"


def translate(text: str):
    def translate(text: str):
        if text.strip():
            response = requests.get(
                f"https://api.52vmy.cn/api/query/fanyi?msg={text.strip()}"
            )
            json_data = response.json()

            if json_data["code"] == 200:
                easygui.msgbox(
                    f"""翻译文本: {text}
翻译结果: {json_data['data']['target']}"""
                )

    threading.Thread(target=translate, args=(text,)).start()


# 实现按钮功能
def new_file():  # 新文件
    global edit_box, filename
    edit_box.delete(1.0, tk.END)
    filename = "Unnamed.py"


def read_file():  # 读取文件
    global edit_box, filename
    filename2 = askopenfilename(defaultextension=".py")
    if filename2 != "":
        with open(
            filename2, "r", encoding="utf-8", errors="ignore"
        ) as f:
            edit_box.delete(1.0, tk.END)  # delete all
            edit_box.insert(1.0, f.read())
            filename = filename2


def to_save_file():  # 另存文件
    global edit_box, filename
    filename = asksaveasfilename(
        initialfile=filename, defaultextension=".py"
    )
    if filename != "":
        with open(filename, "w", encoding="utf-8") as fh:
            msg = edit_box.get(1.0, tk.END)
            fh.write(msg)


# 为按钮设置功能
new_file_button["command"] = lambda: new_file()
read_file_button["command"] = lambda: read_file()
to_save_file_button["command"] = lambda: to_save_file()


# 运行python文件
def runpy():
    global edit_box, textMess, count
    count += 1
    try:
        msg = edit_box.get(1.0, tk.END)
        mg = globals()
        ml = locals()
        print(
            f'第{count}次运行, {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}'
        )
        exec(msg, mg, ml)
    except Exception as e:
        print(f"报错了!报错信息:\n {str(e)}")
        messagebox.showerror("错误", f"报错了!报错信息:\n {str(e)}")


class Tools:
    def __init__(self, box):
        self.box = box

    def format_json(self, event=None):
        # 多行输入
        json_text = (
            text
            if (
                text := (
                    easygui.textbox(
                        "请输入JSON(Java Script Object Notation)：",
                        "格式化JSON(Java Script Object Notation)",
                    )
                )
            )
            else "{}"
        )
        json_text = str(json.loads(json_text))
        # 格式化JSON
        formatted_json = json.dumps(json_text, indent=4)
        # 输出结果
        easygui.msgbox(
            formatted_json,
            "格式化JSON(Java Script Object Notation)",
        )

    def encode_base64(self, event=None):
        # 多行输入
        text = (
            text
            if (
                text := (
                    easygui.textbox("请输入需要编码的文本：", "base64编码")
                )
            )
            else ""
        )
        # 编码
        encoded_text = text.encode("utf-8")
        encoded_text = base64.b64encode(encoded_text)
        encoded_text = encoded_text.decode("utf-8")
        # 输出结果
        easygui.msgbox(encoded_text, "base64编码")

    def decode_base64(self, event=None):
        # 多行输入
        text = (
            text
            if (
                text := (
                    easygui.textbox("请输入需要解码的文本：", "base64解码")
                )
            )
            else ""
        )
        # 解码
        decoded_text = base64.b64decode(text)
        decoded_text = decoded_text.decode("utf-8")
        # 输出结果
        easygui.msgbox(decoded_text, "base64解码")

    def offset_encode(self, event=None):
        offset, text = easygui.multenterbox(
            "请输入偏移量和文本", "偏移量编码", ["偏移量", "文本"]
        )
        new = ""
        offset = int(offset)
        for i in text:
            new += chr(ord(i) + offset)
        easygui.msgbox(new, "偏移量编码")

    def offset_decode(self, event=None):
        offset, text = easygui.multenterbox(
            "请输入偏移量和文本", "偏移量解码", ["偏移量", "文本"]
        )
        new = ""
        offset = int(offset)
        for i in text:
            new += chr(ord(i) - offset)
        easygui.msgbox(new, "偏移量解码")

    def copy(self):
        global root
        edit_box.event_generate("<<Copy>>")

    def cut(self):
        global root
        edit_box.event_generate("<<Cut>>")

    def paste(self):
        global root
        edit_box.event_generate("<<Paste>>")

    def about_author(self):
        easygui.msgbox(
            """
                            开发人员:郭芸龙
                            灵感来源:一名程序员(code.xdf.cn/home), 暗空工作室(code.xdf.cn/home)的成员
                            开发时间:2024-4-1
                            开发工具:Microsoft Visual Studio Code
                            开发语言:Python
                            项目以开源至https://github.com/GuoYunLong20140602/Let-s-Code-Editor-Python
                            """,
            "关于作者",
        )

    def version(self):
        messagebox.showinfo(
            "版本信息",
            """
                            版本号:9.7.7
                            """,
        )


runpy_button["command"] = lambda: runpy()

# 菜单栏
menu_bar = tk.Menu(root, tearoff=0)

tools = Tools(edit_box)
edit_box.bind("<Control-c>", lambda event: tools.copy())
edit_box.bind("<Control-x>", lambda event: tools.cut())
edit_box.bind("<Control-v>", lambda event: tools.paste())
edit_box.bind("<Control-b>", lambda event: runpy())
edit_box.bind("<Control-s>", lambda event: to_save_file())
edit_box.bind("<Control-o>", lambda event: read_file())
edit_box.bind("<Control-n>", lambda event: new_file())
edit_box.bind("<Control-q>", lambda event: root.quit())


def change_bg(event=None):
    new_bg = askcolor().getcolor()
    global edit_box, root
    edit_box.configure(bg=new_bg)
    root.configure(bg=new_bg)


def change_fg(event=None):
    new_fg = askcolor().getcolor()
    global edit_box
    edit_box.configure(fg=new_fg)


def change_font(event=None):
    new_font = easygui.enterbox("请输入字体名", "字体设置")
    global edit_box
    edit_box.configure(font=(new_font, 17))


edit_box.bind("<Control-Shift-Left>", lambda event: change_bg())
edit_box.bind(
    "<Control-Shift-Right>", lambda event: change_fg()
)


def change_font_size(event=None, mode=1):
    global edit_box
    if mode == 1:
        size = int(edit_box.cget("font").split()[1]) + 1
        edit_box.configure(
            font=(edit_box.cget("font").split()[0], size)
        )

    elif mode == -1:
        size = int(edit_box.cget("font").split()[1]) - 1
        edit_box.configure(
            font=(edit_box.cget("font").split()[0], size)
        )


edit_box.bind(
    "<Control-Shift-Up>", lambda event: change_font_size(mode=1)
)
edit_box.bind(
    "<Control-Shift-Down>",
    lambda event: change_font_size(mode=-1),
)

# 文件栏
file_bar = tk.Menu(menu_bar, tearoff=0)
file_bar.add_command(label="新建", command=new_file)
file_bar.add_command(label="打开", command=read_file)
file_bar.add_command(label="另保存", command=to_save_file)
file_bar.add_separator()
file_bar.add_command(label="退出", command=root.quit)
settings = tk.Menu(file_bar, tearoff=0)
file_bar.add_cascade(label="设置", menu=settings)
settings.add_command(label="字体大小", command=change_font_size)
settings.add_command(label="字体颜色", command=change_fg)
settings.add_command(label="背景颜色", command=change_bg)
settings.add_command(label="字体设置", command=change_font)
about = tk.Menu(settings, tearoff=0)
settings.add_cascade(label="关于", menu=about)
about.add_command(label="关于作者", command=tools.about_author)
about.add_command(label="版本信息", command=tools.version)

menu_bar.add_cascade(label="文件", menu=file_bar)
# 编辑栏
edit_bar = tk.Menu(menu_bar, tearoff=0)
edit_bar.add_command(label="复制", command=lambda: tools.copy())
edit_bar.add_command(label="剪切", command=lambda: tools.cut())
edit_bar.add_command(label="粘贴", command=lambda: tools.paste())


menu_bar.add_cascade(label="编辑", menu=edit_bar)
tools_bar = tk.Menu(edit_bar, tearoff=0)
tools_bar.add_command(
    label="格式化JSON", command=lambda: tools.format_json()
)
base64_bar = tk.Menu(tools_bar, tearoff=0)
base64_bar.add_command(
    label="base64编码", command=lambda: tools.encode_base64()
)
base64_bar.add_command(
    label="base64解码", command=lambda: tools.decode_base64()
)
offset_bar = tk.Menu(tools_bar, tearoff=0)
offset_bar.add_command(
    label="偏移量编码", command=lambda: tools.offset_encode()
)
offset_bar.add_command(
    label="偏移量解码", command=lambda: tools.offset_decode()
)
tools_bar.add_command(
    label="翻译",
    comm和=lambda: translate(
        easygui.textbox("请输入要翻译的内容", "翻译")
    ),
)

tools_bar.add_cascade(label="偏移量加密/解密", menu=offset_bar)
tools_bar.add_cascade(label="base64", menu=base64_bar)

menu_bar.add_cascade(label="工具", menu=tools_bar)

about_bar = tk.Menu(menu_bar, tearoff=0)
about_bar.add_command(label="关于作者", command=tools.about_author)
about_bar.add_command(label="版本信息", command=tools.version)
menu_bar.add_cascade(label="关于", menu=about_bar)
root.config(menu=menu_bar)
# 运行主循环
root.mainloop()
