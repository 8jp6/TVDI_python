import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
import tkintermapview as tkmap
from PIL import Image,ImageTk

class MyCustomDialog(Dialog):
    def __init__(self, parent, record:list, title = None):
       print('HI mycustomdialog')
       print(f'傳過來的record:{record}')
       self.lat = float(record["values"][4])
       self.lon = float(record["values"][5])
       super().__init__(parent = parent, title = title) 

    def body(self,master):

        map_frame = ttk.Frame(master)
        map_widget = tkmap.TkinterMapView(map_frame,
                                         width=600,
                                         height=600,
                                         corner_radius=30
                                         )
        map_widget.set_position(self.lat,self.lon,marker=True)
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
