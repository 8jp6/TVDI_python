import datasource
from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============
        
        #==============top Frame===============

        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='空氣品質指標歷史資料',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self)
        sitenames = datasource.get_sitename()
        self.selected_site = tk.StringVar()
        print(sitenames)

        sitenames_cb = ttk.Combobox(bottomFrame,textvariable=self.selected_site)
        sitenames_cb.configure(values=sitenames,state='readonly')
        sitenames_cb.set('選戰點')
        sitenames_cb.bind('<<ComboboxSelected>>',self.sitename_selected)
        sitenames_cb.pack(side='left',expand=True,anchor='n')

        columns = ('date', 'country','aqi','pm2.5','status','lat','long')
        self.tree = ttk.Treeview(bottomFrame,columns=columns, show='headings')

        self.tree.heading('date', text='日期')
        self.tree.heading('country', text='縣市')
        self.tree.heading('aqi', text='AQI')
        self.tree.heading('pm2.5', text='pm2.5')
        self.tree.heading('status', text='狀態')
        self.tree.heading('lat', text='緯度')
        self.tree.heading('long', text='經度')
        #ctrl+F2一次全選同樣的字
        self.tree.column('date', width=120,anchor='center')
        self.tree.column('country', width=100,anchor='center')
        self.tree.column('aqi', width=50,anchor='center')
        self.tree.column('pm2.5', width=50,anchor='center')
        self.tree.column('status', width=50,anchor='center')
        self.tree.column('lat', width=100,anchor='center')
        self.tree.column('long', width=100,anchor='center')
        

        # contacts=[]
        # for n in range(1,100):
        #     contacts.append((f'first{n}',f'last{n}',f'email{n}example.com'))

        # for contact in contacts:
        #     tree.insert('',tk.END,values=contact)

        self.tree.pack(side='right')
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)
        #==============end bottomFrame===============
    
    def sitename_selected(self,event):
        selected = self.selected_site.get()
        selected_data = datasource.get_selected_data(selected)
        for record in selected_data:
            self.tree.insert('','end',values=record)




    
        

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()