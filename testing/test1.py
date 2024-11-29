import requests
import csv
import os
import sys

def get_exe_dir():
    """取得執行檔所在的目錄"""
    if getattr(sys, 'frozen', False):  # 是否被 PyInstaller 打包
        return os.path.dirname(sys.executable)  # 取得 exe 所在目錄
    else:
        return os.path.dirname(os.path.abspath(__file__))  # 取得 .py 檔所在目錄

# 設定檔案路徑
current_dir = get_exe_dir()
file_path = os.path.join(current_dir, '股票.csv')

url = 'https://openapi.twse.com.tw/v1/opendata/t187ap05_L'
data = requests.get(url)
dj = data.json()
with open(file_path,'w',encoding='utf-8',newline='') as f:
    fieldnames = ['公司代號','公司名稱','出表日期','營業收入-上月比較增減(%)','營業收入-上月營收','營業收入-去年同月增減(%)','營業收入-去年當月營收','營業收入-當月營收','產業別','累計營業收入-前期比較增減(%)','累計營業收入-去年累計營收','累計營業收入-當月累計營收','資料年月','備註']
    dict_writer = csv.DictWriter(f,fieldnames=fieldnames)
    dict_writer.writeheader()
    for i in dj:
        dict_writer.writerow(i)