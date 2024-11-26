from pyproj import Transformer
from geopy.geocoders import Nominatim
import sqlite3
import requests
from requests import Response
from pyproj import Proj, transform
import functoins
import time


def xytransform(twx1:float,twy1:float):
    """
    把台灣座標x1y1轉換成世界座標
    """
    # 創建轉換器
    transformer = Transformer.from_crs("epsg:3826", "epsg:4326")
    twd97_x = twx1
    twd97_y = twy1
    # 轉換 TWD97 到 WGS84
    latitude,longitude = transformer.transform(twd97_x, twd97_y)

    print(f'2.TWD97轉WGS84: Latitude: {latitude:.7}, Longitude: {longitude:.7}')
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
    print(f'3.單次轉換結果{list_address}')
    list.append(list_address)
    print(f'4.總清單:{list}')
    return list_address


def latlonturn(mode,list:list = None,x = None,y = None) -> str:
    """
    參數 mode 必須是 'reverse' 或 'observe'。
    從台灣座標x1y1轉換成地址並拆開成 台灣 000 台北市 XXX XX區
    """
    valid_modes = ["reverse", "observe"]
    if mode not in valid_modes:
        raise ValueError(f"無效的模式：{mode}。可接受的模式有：{', '.join(valid_modes)}")

    if mode == "reverse":
        print("1.執行反轉操作")
        latitude, longitude = xytransform(x,y)
        location = get_address_from_coordinates(latitude, longitude)
        address = reverseaddress(location,list)
        return address
    elif mode == "observe":
        print("執行順序操作 沒有這個部分")

#######################################################################################

def download_data_coordinates():
    '''得到coordinates裡面的資料 並且把資料插入到tperoad.db裡面的coordinates table 大概3分鐘'''
    print('按鈕被按了')
    try:
        '''得到RESPONSE'''
        url = "https://tpnco.blob.core.windows.net/blobfs/Rally/TodayUrgentCase.json"
        response:Response = requests.get(url)
        data = response.json()
        # print(response.text)

        '''得到資料裡面的coordinates
        [['10967113574169', 308552.16, 2773353.307],
        ['10967113574169', 308546.447, 2773362.631]] 
        第0個欄位是座標屬於的資料'''
        result = []
        # 遍歷 features 中的每個 JSON 物件
        for feature in data["features"]:
            # 提取該 feature 的 geometry["0"] 中的所有座標
            coordinates_list = feature["geometry"]["coordinates"][0]
            # 提取該 feature 的 BILL_CODE
            bill_code = feature["properties"]["BILL_CODE"]
            # 遍歷每個座標，將 BILL_CODE 和座標結合，並加入結果列表
            for coordinates in coordinates_list:
                result.append([bill_code] + coordinates)
            # 顯示結果
        # print(result)

        '''把COORDINATES裡面的座標換成經緯度'''
        coordinates_dict = {}
        for item in result:
            # 取出每筆資料的編號（例如 '10967113574169'）
            identifier = item[0]
            # 取得對應的坐標資料 (x, y)
            coordinates = [item[1], item[2]]
            
            # 如果這個編號已經在字典裡，則將新的坐標資料加到現有的列表中
            if identifier not in coordinates_dict:
                coordinates_dict[identifier] = []  # 如果該編號還沒有資料，創建一個空列表
            coordinates_dict[identifier].append(coordinates)

        # print(coordinates_dict)

        ###############################################################################

        # 定義 TWD97 和 WGS84 座標系統
        twd97 = Proj(init='epsg:3826')  # TWD97
        wgs84 = Proj(init='epsg:4326')  # WGS84

        # 假設有多筆 TWD97 坐標 [[x1, y1], [x2, y2], ...]
        db_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\readme_proj\TPEroad.db'
        conn = sqlite3.connect(db_path)
        with conn:
            cursor = conn.cursor()
            # 轉換所有 TWD97 坐標為 WGS84
            coordinates_wgs84 = []
            for key, value in coordinates_dict.items():
                keyy = key
                for x, y in value:
                    # 轉換為 WGS84 坐標
                    longitude, latitude = transform(twd97, wgs84, x, y)
                    coordinates_wgs84.append([longitude, latitude])
                    sql = '''
                    INSERT INTO coordinates (BILL_CODE, lat, lon)
                    SELECT ?, ROUND(?, 6), ROUND(?, 6)
                    WHERE NOT EXISTS (
                        SELECT 1 FROM coordinates WHERE lat = ROUND(?, 6)
                    );
                    '''
                    cursor.execute(sql, (keyy, latitude, longitude, latitude))
            


    except Exception as e:
        print(e)

##########################################################################################
    
def download_data():
    '''
    下載資料 需要做驗證只寫入不在資料庫裏面的那筆
    '''
    db_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\readme_proj\TPEroad.db'
    conn = sqlite3.connect(db_path)
    
    url = 'https://tpnco.blob.core.windows.net/blobfs/Rally/TodayUrgentCase.json'
    try:
        response = requests.get(url)
        data = response.json()
        response.raise_for_status()
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Bill_code TEXT,
                RCVdate TEXT,
                Start_date TEXT,
                End_date TEXT,
                Address1 TEXT,
                X1 TEXT,
                Y1 TEXT,
                新地址 TEXT,
                行政區 TEXT,
                Lat TEXT,
                Lon TEXT,
                申請日期 TEXT CHECK (申請日期 LIKE '____-__-__'),
                開始日期 TEXT CHECK (開始日期 LIKE '____-__-__'),
                結束日期 TEXT CHECK (結束日期 LIKE '____-__-__'),
                UNIQUE(Address1,RCVdate)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS coordinates (
                Bill_code TEXT,
                Lat TEXT,
                Lon TEXT
            )
            ''')
            print("Table 'records' created or already exists.")

    except Exception as e:
        print(e)

    else:
        with conn:
            cursor = conn.cursor()
            for i in data['features']:
                for k in i['properties']:
                    Bill_code:str = i['properties']["BILL_CODE"]
                    RCVdate = i['properties']["URGENT_RCV_DATE"]
                    Start_date = i['properties']["URGENT_START_DATE"]
                    End_date = i['properties']["URGENT_END_DATE"]
                    Address1 = i['properties']["URGENT_ADDRESS1"]
                    X1 = i['properties']["X1"]
                    Y1 = i['properties']["Y1"]
                    formatted_RCVdate = f"{RCVdate[:4]}-{RCVdate[4:6]}-{RCVdate[6:8]}" if RCVdate else None
                    formatted_Start_date = f"{Start_date[:4]}-{Start_date[4:6]}-{Start_date[6:8]}" if Start_date else None
                    formatted_End_date = f"{End_date[:4]}-{End_date[4:6]}-{End_date[6:8]}" if End_date else None

                    
                    cursor = conn.cursor()
                    sql = '''INSERT OR IGNORE INTO records(Bill_code, RCVdate, Start_date, End_date, Address1, X1, Y1,申請日期, 開始日期, 結束日期)
                                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                            '''
                    cursor.execute(sql,(Bill_code, RCVdate, Start_date, End_date, Address1, X1, Y1,formatted_RCVdate, formatted_Start_date, formatted_End_date))

    return print('資料下載，匯入完成')

##############################################################################################
def old_to_new_address():
    conn = sqlite3.connect(r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\readme_proj\TPEroad.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT Address1,x1,y1 FROM records''')
        # 把地址跟x1y1座標存進一個字典裡面
        address = []
        for i in cursor.fetchall():
            di = {}
            di["地址"] = i[0]
            di["x1"] = i[1]
            di["y1"] = i[2]
            address.append(di)
        print(address)

        alladdress = []

        for i in address:
            ad = i['地址']
            fuad = functoins.latlonturn("reverse",alladdress,i['x1'],i['y1'])
            fullstreet = ''.join(fuad)
            lat,lon = functoins.xytransform(i['x1'],i['y1'])
            for i in fuad:
                if "區" in i :dist = i
            add_content_sql = '''
            UPDATE RECORDS
            SET 新地址 = ?, 行政區 = ?, Lat = ?, Lon = ?
            WHERE address1 = ?;
            '''

            cursor.execute(add_content_sql,(fullstreet, dist, lat, lon, ad))
            time.sleep(2)
            conn.commit()
        cursor.execute('''UPDATE records SET 行政區 = '大安區' WHERE 行政區 = '東區地下街';''')
#############################################################################################

def get_district()->list[str]:
    '''
    docString
    parameter:
    return:
        傳出所有的行政區名稱
    '''
    conn = sqlite3.connect("TPEroad.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT 行政區
        FROM records
        '''
        # Execute the SQL query
        cursor.execute(sql)
        # Get all results and extract first item from each row into a list
        district = [items[0] for items in cursor.fetchall()]
    
    # Return the list of unique sitenames
    return district

def get_rodename(district:str)->list[str]:
    '''
    docString
    parameter:
        county:行政區名稱

    return:
        傳出行政區內所有登記的路段
    '''
    conn = sqlite3.connect("TPEroad.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT 新地址
        FROM records
        WHERE district = ?       
         '''
        # Execute the SQL query
        cursor.execute(sql,(district,))       
        full_address = [items[0] for items in cursor.fetchall()]
        
    
    # Return the list of unique sitenames
    return full_address

def get_selected_data(district:str)->list[list]:
    '''
    使用者選擇了disritct,並將district傳入
    Parameter:
        district: 站點的名稱
    Return:
        所有關於此站點的相關資料
    '''
    conn = sqlite3.connect("TPEroad.db")
    with conn:
        cursor = conn.cursor()        
        sql = '''
        SELECT 申請日期,
        開始日期,
        結束日期,
        新地址,
	    PRINTF("%.4f", ROUND(lat, 4)) AS Lat ,
        PRINTF("%.4f", ROUND(lon, 4)) as Lon 
        FROM records
        WHERE 行政區=?
        ORDER BY RCVdate DESC;
        '''
        cursor.execute(sql,(district,))
        address_list = [list(item) for item in cursor.fetchall()]
        return address_list
    