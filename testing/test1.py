import requests
import csv
import os
import sys
import pandas as pd

def get_exe_dir():
    """取得執行檔所在的目錄"""
    if getattr(sys, 'frozen', False):  # 是否被 PyInstaller 打包
        return os.path.dirname(sys.executable)  # 取得 exe 所在目錄
    else:
        return os.path.dirname(os.path.abspath(__file__))  # 取得 .py 檔所在目錄

# 設定檔案路徑
current_dir = get_exe_dir()
file_path = os.path.join(current_dir, 'merged_sorted_data.csv')

custom_fieldnames = {
    '公司代號': '公司代號',
    '公司名稱': '公司名稱',
    '出表日期': '出表日期',
    '營業收入-上月比較增減(%)': '上月比較增減(%)',
    '營業收入-上月營收': '上月營收',
    '營業收入-去年同月增減(%)': '去年同月增減(%)',
    '營業收入-去年當月營收': '去年當月營收',
    '營業收入-當月營收': '當月營收',
    '產業別': '產業別',
    '累計營業收入-前期比較增減(%)': '累計營業收入-前期比較增減(%)',
    '累計營業收入-去年累計營收': '累計營業收入-去年累計營收',
    '累計營業收入-當月累計營收': '累計營業收入-當月累計營收',
    '資料年月': '資料年月',
    '備註': '備註'
}


url1 = 'https://openapi.twse.com.tw/v1/opendata/t187ap05_L' #上市
url2 = 'https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_O' #上櫃
response1 = requests.get(url1)
response2 = requests.get(url2)
data1 = pd.DataFrame(response1.json())
data2 = pd.DataFrame(response2.json())
merged_data = pd.concat([data1, data2], ignore_index=True)

# 根據項目編號遞增排序 (假設欄位名稱是 'item_id')
sorted_data = merged_data.sort_values(by='公司代號')



with open(file_path,'w',encoding='utf-8-sig',newline='') as f:
    fieldnames = ['公司代號','公司名稱','出表日期','營業收入-上月比較增減(%)','營業收入-上月營收','營業收入-去年同月增減(%)','營業收入-去年當月營收','營業收入-當月營收','產業別','累計營業收入-前期比較增減(%)','累計營業收入-去年累計營收','累計營業收入-當月累計營收','資料年月','備註']
    custom_fieldnames_list = list(custom_fieldnames.values())
    dict_writer = csv.DictWriter(f,fieldnames=custom_fieldnames_list)
    dict_writer.writeheader()
    for _, row in sorted_data.iterrows():
        # 根據自訂欄位名稱對應值，重新生成字典
        custom_row = {custom_fieldnames[key]: row[key] for key in fieldnames if key in row}
        dict_writer.writerow(custom_row)