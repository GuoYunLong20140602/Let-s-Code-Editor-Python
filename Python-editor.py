code# 一个简单的Python代码编辑器, 可运行程序
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()


root.geometry("1000x700+0+0")
root.resizable(0, 0)  # 禁止调整窗口大小，防止出现滚动条影响美观。
root.title("Let' Code-Editor-Python")


# 创建一个文本框，用于显示和编辑代码。
edit_box = tk.Text(root, font=("Consolas", 20), width=1000, height=700, wrap="none")

edit_box.place(x=0, y=0, anchor="nw")  # 使用place布局，因为滚动条是绝对定位的。


class Commands:
    def __init__(self, input_box):
        self.box = input_box  # 保存输入框的引用。

    def save_file(self):  # 保存文件。
        path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python文件", "*.py")],
        )
        print(path)
        text = self.box.get(1.0, "end")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)  # 写入文本。

    def open_file(self):
        path = filedialog.askopenfilename(
            defaultextension="py", filetypes=[("Python文件", "*.py")]
        )  # 打开文件。
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()  # 读取文本。
        self.box.delete(1.0, "end")
        self.box.insert("end", code)


# 菜单栏
menu_bar = tk.Menu(
    root,
    background="red",
    foreground="white",
    activebackground="blue",
    activeforeground="white",
)  # 设置菜单栏的样式。

commands = Commands(edit_box)  # 创建一个Commands对象。

# 添加file_bar
file_bar = tk.Menu(
    menu_bar, tearoff=0, background="red", foreground="white"
)  # 设置file_bar的样式。
file_bar.add_command(label="保存文件", command=commands.save_file)  # 添加保存命令。
file_bar.add_command(label="打开文件", command=commands.open_file)  # 添加打开命令。
menu_bar.add_cascade(label="文件", menu=file_bar)  # 将file_bar添加到菜单栏。

root.config(menu=menu_bar)


root.mainloop()
