from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkintermapview import TkinterMapView
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk  # 使用 Pillow
import matplotlib.pyplot as plt  # 繪製圖表
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from proj_proj import draw_decision_tree, rf_model, features, label_map, get_model_metrics,X ,y, load_data

import sys
import pandas as pd


class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("動態圖像介面")

        # 綁定窗口關閉事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.new_buttons = [] 

        # 載入資料
        self.data, self.counties, self.regions = load_data()

        # 預先計算模型數據
        print("正在計算模型數據，請稍候...")
        self.report, self.scores, self.accuracy = get_model_metrics(rf_model, X, y, label_map)
        print("模型數據計算完成！")

        # 地圖組件
        self.map_view = None

        #============================================================================
        # 左側框架
        self.left_frame = tk.Frame(self)
        #============================================================================
        # 子框架 1: 放置決策樹按鈕和新按鈕
        self.frame1 = tk.Frame(self.left_frame)
        self.frame1.grid(row=0, column=0, pady=5)

        # 按鈕
        button1 = tk.Button(self.frame1,
                            text="決策樹",
                            command=lambda: (self.reset_ui(),self.draw_tree_in_gui(), self.create_new_button()))
        button1.grid(row=0, column=0, padx=5)
        button2 = tk.Button(self.left_frame,
                            text="詳細結果", 
                            command=lambda:(self.reset_ui(),self.show_metrics_in_right_frame()))
        button2.grid(row=1, column=0, pady=5)
        button3 = tk.Button(self.left_frame, 
                            text="重新整理",
                            command=self.reset_ui)        
        button3.grid(row=2, column=0, pady=5)
        self.radio_frame = tk.Frame(self.left_frame)
        self.radio_frame.grid(row=5, column=0, pady=5)

        # 下拉式選單
        self.selected_county = tk.StringVar(self)
        self.selected_county.set("選擇縣市")  # 預設值
        dropdown = ttk.Combobox(self.left_frame, textvariable=self.selected_county, values=self.counties)
        dropdown.bind("<<ComboboxSelected>>", self.update_radiobuttons)        
        dropdown.grid(row=3, column=0, pady=5)

        #============================================================================
        self.left_frame.grid_columnconfigure(0, minsize=1)
        self.left_frame.pack(side="left",padx=5,pady=5)
        #============================================================================
        # 右側框架
        self.right_frame = tk.Frame(self)
        #============================================================================
        # 右側初始圖片
        self.image = Image.open(r"C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\gogoro-muji-3-768x439.jpg")  # 替換成你的圖片路徑
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.right_frame, image=self.photo)
        self.label.pack()
        #============================================================================
        self.right_frame.pack(side="bottom", fill="both", expand=True, pady=5)
        #============================================================================


    def draw_tree_in_gui(self):
        print("draw_tree_in_gui activates")
        # 清空右側框架的舊內容
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 呼叫 proj_proj 的繪圖函式
        fig = draw_decision_tree(rf_model, features, list(label_map.keys()),fullscreen=False)
        print("draw_decision_tree activates")

        # 將 Matplotlib 圖嵌入到 Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_new_button(self):
        print("create_new_button activates")
        # 動態生成按鈕
        new_button = tk.Button(self.frame1, text="放大數據",command=self.new_button_action)
        new_button.grid(row=0, column=1, padx=5)
        self.new_buttons.append(new_button) 

    def show_metrics_in_right_frame(self):
        # 將報告轉換為 DataFrame
        report_df = pd.DataFrame(self.report).transpose().reset_index()

        # 清空右側框架的舊內容
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 上方數據摘要
        summary_text = f"模型準確率: {self.accuracy:.2f}\n"
        summary_label = tk.Label(self.right_frame, text=summary_text, justify="left", font=("Arial", 12))
        summary_label.pack(anchor="w", padx=10, pady=5)

        # 定義 Treeview 的列名
        columns = ["Category"] + list(report_df.columns[1:])  # 顯式定義列名

        # 創建 Treeview
        tree = ttk.Treeview(self.right_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        # 插入數據
        for _, row in report_df.iterrows():
            # 獲取第一列的 "index"
            index_value = row["index"]

            if index_value == "accuracy":
                # 如果是 accuracy，保留倒數第二列 (f1-score) 和最後一列 (support)，其餘填充 "-"
                formatted_values = [index_value] + ["-"] * (len(row) - 3) + [
                    f"{row.iloc[-2]:.6f}",
                    f"{row.iloc[-1]:.6f}"
                ]
            else:
                # 格式化數據，限制到小數第六位
                formatted_values = [index_value] + [
                    f"{x:.6f}" if isinstance(x, float) else x for x in row.iloc[1:]
                ]

            # 插入到 Treeview
            tree.insert("", "end", values=formatted_values)


        tree.pack(fill="both", expand=True, padx=10, pady=10)



    def reset_ui(self):
        # 刪除所有新按鈕
        for btn in self.new_buttons:
            btn.destroy()
        self.new_buttons.clear()

        # 恢復 right_frame 為原始圖片
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 清除無線電按鈕
        for widget in self.radio_frame.winfo_children():
            widget.destroy()

        # cbbox預設文字
        self.selected_county.set("選擇縣市") 

        # 清空右上角的長條圖
        if hasattr(self, "right_top_frame") and self.right_top_frame.winfo_children():
            for widget in self.right_top_frame.winfo_children():
                widget.destroy()

        # 如果需要刪除 `right_top_frame`，可用這段代碼
        if hasattr(self, "right_top_frame"):
            self.right_top_frame.destroy()
            del self.right_top_frame


        self.image = Image.open(r"C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\gogoro-muji-3-768x439.jpg")  # 替換成你的圖片路徑
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.right_frame, image=self.photo)
        self.label.pack()

    #新按鈕動作
    def new_button_action(self):
        print("new_buttomn_action activates")
        draw_decision_tree(rf_model, features, list(label_map.keys()),figsize=(15, 10),fullscreen=True)

    def update_radiobuttons(self, event):
        # 清空旧的单选按钮
        for widget in self.radio_frame.winfo_children():
            widget.destroy()

        # 清空右側框架的舊內容
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 获取所选县市
        selected_county = self.selected_county.get()
        regions = self.regions.get(selected_county, [])
        print(f"Selected county: {selected_county}, Regions: {regions}")  # 調試輸出
        
        # 動態生成單選按鈕，兩欄佈局
        self.selected_region = tk.StringVar(value="NoneSelected")
        print(f"Initial selected_region value: {self.selected_region.get()}")  # 調試輸出
        
        col_count = 2  # 設定兩欄
        for idx, region in enumerate(regions):
            row = idx // col_count  # 決定行數
            col = idx % col_count  # 決定列數
            rb = tk.Radiobutton(
                self.radio_frame,
                text=region,
                variable=self.selected_region,
                value=region,
                command=lambda r=region: self.display_region_data(r),
                anchor="w",
                padx=10,
            )
            rb.grid(row=row, column=col, sticky="w", padx=5, pady=5)

        if self.map_view:self.map_view.destroy()
        if self.label:self.label.destroy()

        # 初始化地圖組件
        self.map_view = TkinterMapView(self.right_frame, width=800, height=500, corner_radius=30)
        self.map_view.set_position(deg_x=25.033, deg_y=121.56)  # 設定地圖中心點（台灣範圍）
        self.map_view.set_zoom(10)
        self.map_view.pack(fill="both", expand=True)
        

    def display_region_data(self, region):
        # 如果 right_top_frame 尚未創建，則動態創建
        if not hasattr(self, "right_top_frame"):
            self.right_top_frame = tk.Frame(self)
            self.right_top_frame.pack(side="top", fill="x", pady=5)

        # 清空 right_top_frame 的舊內容
        if self.right_top_frame.winfo_children():
            for widget in self.right_top_frame.winfo_children():
                widget.destroy()


        # 從數據中查找對應區域的資訊
        region_data = self.data[self.data['區域別'] == region].iloc[0]

        # 從數據中找到對應城區
        self.selected_town = str(self.selected_region.get())
        print(self.selected_town)

        # 從 StringVar 中提取選擇的縣市
        selected_county_value = self.selected_county.get()
        print(selected_county_value)

        # 拼接完整的地點名稱
        self.selected_place = selected_county_value + self.selected_town
        print(self.selected_place)

            # 更新地圖
        if self.map_view:
            self.update_map(self.selected_place)

        # 提取 2024 人口數、土地面積、電車登記
        car_registration = region_data['電車登記數']
        charge_station = region_data['站點小計']
        rec_amounts = int(car_registration/125)

        # 在右側框架顯示數據
        for widget in self.right_top_frame.winfo_children():
            widget.destroy()  # 清空舊內容

        # 創建 Matplotlib 橫向長條圖
        fig = Figure(figsize=(6, 2), dpi=100)
        ax = fig.add_subplot(111)

        # 數據和標籤
        categories = ['電車登記數','站點數','最佳車站數']
        values = [car_registration,charge_station,rec_amounts]

        # 畫橫向長條圖
        bars = ax.barh(categories, values, color=['blue', 'orange', 'green'])
        ax.set_title(f"{region} 數據概覽", fontsize=14)
        ax.set_xlabel("數值", fontsize=12)

        # 在每個長條上顯示數值
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 1,  # 數值偏移量，避免與長條重疊
                bar.get_y() + bar.get_height() / 2,  # 總高度的中間
                f'{width}',  # 顯示小數點後兩位
                va='center',  # 垂直對齊
                ha='left',  # 水平對齊
                fontsize=10,
                color='black'
            )

        # 嵌入到 Tkinter 中
        canvas = FigureCanvasTkAgg(fig, master=self.right_top_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def update_map(self, district):
        """更新地圖以顯示指定行政區的站點"""

        stations_file = r"C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\新Gogoro_站點整理.xlsx"
        districts_file = r"C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\行政區經緯度.xlsx"

        # 加載數據
        self.stations_data = pd.read_excel(stations_file)
        self.districts_data = pd.read_excel(districts_file)
        

        if not district:
            return

        # 查找行政區中心點
        district_info = self.districts_data[self.districts_data["城區"] == district]
        if district_info.empty:
            return

        center_latitude = district_info.iloc[0]["緯度"]
        center_longitude = district_info.iloc[0]["經度"]

        # 清除地圖上的所有標記
        self.map_view.delete_all_marker()

        # 設置地圖位置到行政區中心
        self.map_view.set_position(center_latitude, center_longitude)
        self.map_view.set_zoom(14)

        # 篩選站點數據
        filtered_stations = self.stations_data[self.stations_data["城區"] == district]
        for _, row in filtered_stations.iterrows():
            station_name = row["名稱"]
            latitude = row["緯度"]
            longitude = row["經度"]

            # 添加標記
            if pd.notna(latitude) and pd.notna(longitude):
                self.map_view.set_marker(latitude, longitude, text=station_name)






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