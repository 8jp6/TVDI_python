from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk  # 使用 Pillow
import matplotlib.pyplot as plt  # 繪製圖表
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from proj_proj import draw_decision_tree, rf_model, features, label_map, get_model_metrics,X ,y
import sys
import pandas as pd


class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("動態圖像介面")
        # 綁定窗口關閉事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.new_buttons = [] 

        # 預先計算模型數據
        self.report, self.scores, self.accuracy = get_model_metrics(rf_model, X, y, label_map)

        #============================================================================
        # 左側框架
        self.left_frame = tk.Frame(self)

        # 子框架 1: 放置決策樹按鈕和新按鈕
        self.frame1 = tk.Frame(self.left_frame)
        self.frame1.grid(row=0, column=0, pady=5)

        # 按鈕
        button1 = tk.Button(self.frame1,
                            text="決策樹",
                            command=lambda: (self.draw_tree_in_gui(), self.create_new_button()))
        button1.grid(row=0, column=0, padx=5)
        button2 = tk.Button(self.left_frame,
                            text="詳細結果", 
                            command=self.show_metrics_in_right_frame)
        button2.grid(row=1, column=0, pady=5)
        button3 = tk.Button(self.left_frame, 
                            text="重新整理",
                            command=self.reset_ui)        
        button3.grid(row=2, column=0, pady=5)

        # 下拉式選單
        options = ["選項1", "選項2", "選項3"]
        variable = tk.StringVar(self)
        variable.set(options[0])  # 預設值
        dropdown = ttk.Combobox(self.left_frame, textvariable = variable, values=options)
        dropdown.grid(row=3, column=0, pady=5)

        #============================================================================
        self.left_frame.grid_columnconfigure(0, minsize=1)
        self.left_frame.pack(side="left",padx=5,pady=5)
        #============================================================================
        # 右側框架
        self.right_frame = tk.Frame(self)
        # 右側初始圖片
        self.image = Image.open(r"C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\proj_proj\imageedit_2_6435805884.jpg")  # 替換成你的圖片路徑
        self.photo = ImageTk.PhotoImage(self.image)
        label = tk.Label(self.right_frame, image=self.photo)
        label.pack()
        #============================================================================
        self.right_frame.pack(side="right", padx= 15, pady = 15)
        #============================================================================


    def draw_tree_in_gui(self):
        # 清空右側框架的舊內容
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 呼叫 proj_proj 的繪圖函式
        fig = draw_decision_tree(rf_model, features, list(label_map.keys()))

        # 將 Matplotlib 圖嵌入到 Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_new_button(self):
        # 動態生成按鈕
        new_button = tk.Button(self.frame1, text="放大數據",command=self.new_button_action)
        new_button.grid(row=0, column=1, padx=5)
        self.new_buttons.append(new_button) 

    def show_metrics_in_right_frame(self):
        # 將報告轉換為 DataFrame
        report_df = pd.DataFrame(self.report).transpose().reset_index()

        # 清空 right_frame 的舊內容
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 上方數據摘要
        summary_text = f"平均準確度: {self.scores.mean():.2f}\n模型準確率: {self.accuracy:.2f}\n"
        summary_label = tk.Label(self.right_frame, text=summary_text, justify="left", font=("Arial", 12))
        summary_label.pack(anchor="w", padx=10, pady=5)

        # 創建 Treeview
        columns = report_df.columns
        tree = ttk.Treeview(self.right_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        # 插入數據
        for _, row in report_df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True, padx=10, pady=10)



    def reset_ui(self):
        # 刪除所有新按鈕
        for btn in self.new_buttons:
            btn.destroy()
        self.new_buttons.clear()

        # 恢復 right_frame 為原始圖片
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        self.image = Image.open(r"C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\proj_proj\imageedit_2_6435805884.jpg")  # 替換成你的圖片路徑
        self.photo = ImageTk.PhotoImage(self.image)
        label = tk.Label(self.right_frame, image=self.photo)
        label.pack()

    #新按鈕動作
    def new_button_action(self):
        fig = draw_decision_tree(rf_model, features, list(label_map.keys()),figsize=(15, 10),fullscreen=True)
        fig.show()

    def show_metrics_in_right_frame(self):
        # 獲取模型數據
        report, scores, accuracy = get_model_metrics(rf_model, X, y, label_map)
        df = pd.DataFrame(report).transpose().reset_index()

        # 清空 right_frame 的舊內容
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 上方數據摘要
        summary_text = f"平均準確度: {scores.mean():.2f}\n模型準確率: {accuracy:.2f}\n"
        summary_label = tk.Label(self.right_frame, text=summary_text, justify="left", font=("Arial", 12))
        summary_label.pack(anchor="w", padx=10, pady=5)

        # 創建 Treeview
        columns = df.columns
        tree = ttk.Treeview(self.right_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        # 插入數據
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True, padx=10, pady=10)


    #完整關閉程式
    def on_closing(self):
        print("窗口被關閉")
        self.quit() 
        self.destroy()
        sys.exit()



def main():
    window = Window(theme="arc")
    window.mainloop()
    

if __name__ == '__main__':
    main()