from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk  # 使用 Pillow
import matplotlib.pyplot as plt  # 繪製圖表
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("動態圖像介面")

        #============================================================================
        # 左側框架
        left_frame = tk.Frame(self)

        # 按鈕
        button1 = tk.Button(left_frame, text="決策樹", command=switch_image)
        button1.pack(pady=10)
        button2 = tk.Button(left_frame, text="詳細結果", command=switch_image)
        button2.pack(pady=10)
        button3 = tk.Button(left_frame, text="重新整理", command=switch_image)        
        button3.pack(pady=10)

        # 下拉式選單
        options = ["選項1", "選項2", "選項3"]
        variable = tk.StringVar(self)
        variable.set(options[0])  # 預設值
        dropdown = ttk.Combobox(left_frame, textvariable = variable, values=options)
        dropdown.pack()

        #============================================================================
        left_frame.pack(side="left")
        #============================================================================
        # 右側框架
        right_frame = tk.Frame(self)
        # 右側初始圖片
        self.image = Image.open(r"C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\proj_proj\imageedit_2_6435805884.jpg")  # 替換成你的圖片路徑
        self.photo = ImageTk.PhotoImage(self.image)
        label = tk.Label(right_frame, image=self.photo)
        label.pack()
        #============================================================================
        right_frame.pack(side="right", padx= 15, pady = 15)
        #============================================================================



        # 切換圖片或圖表的函數
        def switch_image(event):
            global label  # 讓函數能修改全域變數 label
            # 移除舊圖片
            label.destroy()

        dropdown.bind("<ButtonRelease-1>", switch_image)




def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()