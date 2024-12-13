import tkinter as tk
from tkintermapview import TkinterMapView
import pandas as pd



def update_map(self, district):
    """更新地圖以顯示指定行政區的站點"""

    stations_file = r"C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\原始資料\新Gogoro_站點整理.xlsx"
    districts_file = r"C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\原始資料\行政區經緯度.xlsx"

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
