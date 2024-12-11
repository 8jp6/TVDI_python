import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView

def create_gui():
    # 創建主視窗
    root = tk.Tk()
    root.title("充電站地圖系統")
    root.geometry("800x600")

    # 左側框架
    left_frame = tk.Frame(root, width=400, height=600, borderwidth=2, relief="groove")
    left_frame.pack(side="left", fill="both", expand=True)

    # 大標題
    title_label = tk.Label(left_frame, text="gogoro站點預測", font=("Arial", 16))
    title_label.pack(pady=10)

    # 線性回歸圖按鈕
    boxplot_button = tk.Button(left_frame, text="線性回歸圖")
    boxplot_button.pack(pady=5)

    # 隨機森林按鈕
    random_forest_button = tk.Button(left_frame, text="隨機森林")
    random_forest_button.pack(pady=5)

    # 選擇框架
    selected_frame = tk.Frame(left_frame, borderwidth=1, relief="solid")
    selected_frame.pack(pady=10, fill="x", padx=10)

    # 行政區下拉式選單
    selected_label = tk.Label(selected_frame, text="行政區下拉式選單")
    selected_label.pack(pady=5)

    dropdown = ttk.Combobox(selected_frame, values=["行政區1", "行政區2", "行政區3"])
    dropdown.pack(pady=5)

    # 總覽行政區的建議情況
    summary_label = tk.Label(selected_frame, text="行政區的未來車輛預測", wraplength=300)
    summary_label.pack(pady=10)

    # 右側框架
    right_frame = tk.Frame(root, width=400, height=600, borderwidth=2, relief="groove")
    right_frame.pack(side="right", fill="both", expand=True)

    # 地圖框架
    mapframe = tk.Frame(right_frame, borderwidth=1, relief="solid")
    mapframe.pack(pady=10, fill="both", expand=True)

    map_label = tk.Label(mapframe, text="充電站地圖點")
    map_label.pack()

    # TkinterMapView 地圖嵌入（需要 tkintermapview 庫）
    map_view = TkinterMapView(mapframe, width=300, height=300)
    map_view.pack(fill="both", expand=True)
    map_view.set_position(25.033964, 121.564468)  # 台北 101 的經緯度
    map_view.set_zoom(12)

    # 運行主視窗
    root.mainloop()

if __name__ == "__main__":
    create_gui()
