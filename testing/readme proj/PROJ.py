from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        self.resizable(True, True)
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============

        #==============top Frame==================
        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='台北市今日使用道路',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self,padding=[10,10,10,10])
        #==============combobxfrmae===============
        self.selectedFrame= ttk.Frame(self,padding=[10,10,10,10])
        #combobox選擇城市      
        counties = datasource.get_county()
        self.selected_county = tk.StringVar()
        sitenames_cb = ttk.Combobox(self.selectedFrame, textvariable=self.selected_county,values=counties,state='readonly')
        self.selected_county.set('請選擇城市')
        sitenames_cb.bind('<<ComboboxSelected>>', self.county_selected)
        sitenames_cb.pack(anchor='n',pady=10)

        self.sitenameFrame = None 

        self.selectedFrame.pack(side='left',padx=(20,0))

        bottomFrame.pack(padx=20,pady=20)
        






















def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()