import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
import tkintermapview as tkmap
from PIL import Image,ImageTk
import sqlite3
import os

class MyCustomDialog(Dialog):
    def __init__(self, parent, record:list, title = None):
       print(f'傳過來的record:{record}')
       self.lat = float(record["values"][4])
       self.lon = float(record["values"][5])
       self.ad = record['values'][3]
       print(self.ad)
       self.get_data()
       self.data = self.address_list
       super().__init__(parent = parent, title = title) 

    def body(self,master):

        map_frame = ttk.Frame(master)
        map_widget = tkmap.TkinterMapView(map_frame, width=600, height=400, corner_radius=0)
        map_widget.set_position(self.lat,self.lon,marker=True)
        # # 畫出範圍的矩形
        map_widget.set_polygon(self.ordered_coordinates,fill_color = '#1e90ff')


        map_widget.pack()
        map_frame.pack(padx=10,pady=10)

    def apply(self):
        print('使用者按了apply')

    def buttonbox(self):
        box = tk.Frame(self)
        self.ok_button = tk.Button(box,text='OK',width=10,command = self.ok,default = tk.ACTIVE)
        self.ok_button.pack(side = tk.LEFT,padx=5, pady=5)
        self.cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>",self.ok)
        self.bind("<Escape>",self.cancel)
        box.pack()

    def ok(self,event = None):
        print('OK被按了')
        super().ok()

    def cancel(self, event = None):
        print('Cancel被按了')
        super().cancel()

    def get_data(self):
        conn = sqlite3.connect(r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\readme_proj\TPEroad.db')
        with conn:
            cursor = conn.cursor()        
        sql = '''
        SELECT c.Lat, c.Lon
        FROM coordinates c
        JOIN records r ON c.Bill_code = r.Bill_code
        WHERE r.新地址 = ?;
        '''
        cursor.execute(sql,(self.ad,))
        self.address_list = [[float(coord) for coord in item] for item in cursor.fetchall()]
        print(self.address_list)
        # 根據經度和緯度來排序座標
        sorted_coordinates = sorted(self.address_list, key=lambda x: (x[0], x[1]))

        # 確定四個角點
        x_values = [coord[0] for coord in sorted_coordinates]
        y_values = [coord[1] for coord in sorted_coordinates]

        # 確定長方形的四個角點
        left_bottom = (min(x_values), min(y_values))
        right_bottom = (max(x_values), min(y_values))
        left_top = (min(x_values), max(y_values))
        right_top = (max(x_values), max(y_values))

        # 用正確的順序繪製長方形的四個角
        self.ordered_coordinates = [left_bottom, left_top, right_top, right_bottom, left_bottom]