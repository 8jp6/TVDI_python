from pyproj import Transformer
from geopy.geocoders import Nominatim
import requests
from requests import Response
import sqlite3
import time


def xytransform(twx1:float,twy1:float):
    """把台灣座標x1y1轉換成世界座標"""
    # 創建轉換器
    transformer = Transformer.from_crs("epsg:3826", "epsg:4326")
    twd97_x = twx1
    twd97_y = twy1
    # 轉換 TWD97 到 WGS84
    latitude,longitude = transformer.transform(twd97_x, twd97_y)
    return latitude, longitude


def get_address_from_coordinates(lat, lon):
    """ 根據經緯度獲取地址或道路名稱 """
    # 初始化 Nominatim 反向地理編碼器
    geolocator = Nominatim(user_agent='PROJ')
    location = geolocator.reverse((lat, lon), language='zh-TW', exactly_one=True)
    if location:
        return location.address
    return "未找到地址"


def reverseaddress(location,alllist:list = None):
    """把取得的地址反轉成台北市在前"""
    list = alllist
    list_address = [item.strip() for item in location.split(",")]
    list_address.reverse()
    print(f'單次轉換結果{list_address}')
    list.append(list_address)
    print(f'總清單:{list}')




def latlonturn(mode,list:list = None,x = None,y = None) -> str:
    """
    參數 mode 必須是 'reverse' 或 'observe'。
    從台灣座標x1y1轉換成地址並拆開成 台灣 000 台北市 XXX XX區
    """
    valid_modes = ["reverse", "observe"]
    if mode not in valid_modes:
        raise ValueError(f"無效的模式：{mode}。可接受的模式有：{', '.join(valid_modes)}")

    if mode == "reverse":
        latitude, longitude = xytransform(x,y)
        location = get_address_from_coordinates(latitude, longitude)
        address = reverseaddress(location,list)
        return address
