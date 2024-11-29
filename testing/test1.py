import requests
import csv
import os

# 取得目前執行檔案的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
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