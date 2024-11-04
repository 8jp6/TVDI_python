import L7datasource
from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False,False)
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
        #==============selectedFrame===============

        self.selectedFrame = ttk.Frame(self,padding=[10,10,10,10])

        countynames = L7datasource.get_county()
        self.selected_site = tk.StringVar()
        self.selected_county = tk.StringVar()
        sitenames_cb = ttk.Combobox(self.selectedFrame,textvariable=self.selected_county)
        sitenames_cb.configure(values=countynames,state='readonly')
        sitenames_cb.set('選城市')
        sitenames_cb.bind('<<ComboboxSelected>>',self.county_selected)
        sitenames_cb.pack(anchor='n',pady=10)

        self.listbox = None

        self.selectedFrame.pack(side='left',expand=True,fill='y',padx=(20,0))
        #==============endselectedFrame===============

        columns = ('date', 'country','aqi','pm2.5','status','long','lat')
        self.tree = ttk.Treeview(bottomFrame,columns=columns, show='headings')

        self.tree.heading('date', text='日期')
        self.tree.heading('country', text='縣市')
        self.tree.heading('aqi', text='AQI')
        self.tree.heading('pm2.5', text='pm2.5')
        self.tree.heading('status', text='狀態')
        self.tree.heading('long', text='經度')
        self.tree.heading('lat', text='緯度')
        #ctrl+F2一次全選同樣的字
        self.tree.column('date', width=120,anchor='center')
        self.tree.column('country', width=100,anchor='center')
        self.tree.column('aqi', width=50,anchor='center')
        self.tree.column('pm2.5', width=50,anchor='center')
        self.tree.column('status', width=50,anchor='center')
        self.tree.column('long', width=100,anchor='center')
        self.tree.column('lat', width=100,anchor='center')


        self.tree.pack(side='right')
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)
        #==============end bottomFrame===============
    
    def sitename_selected(self,event):
        for children in self.tree.get_children():
            self.tree.delete(children)
        selected = self.selected_site.get()
        selected_data = L7datasource.get_selected_data(selected)
        for record in selected_data:
            self.tree.insert('','end',values=record)

    def county_selected(self,event):
        selected = self.selected_county.get()
        counties = L7datasource.get_sitename(county=selected)
        if self.listbox:
            self.listbox.destroy()
        var = tk.Variable(value=counties)
        self.listbox = tk.Listbox(self.selectedFrame, listvariable=var, height=6, selectmode=tk.EXTENDED)
        self.listbox.pack()

            

    
def download():
    L7datasource.get_all_data()
    pass

def main():
    download()
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()