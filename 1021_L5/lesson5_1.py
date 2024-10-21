import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style = ttk.Style(self)        

        style.configure('topfra.TLabel', font = ('arial',20))
        style.configure('TFrame',background ='lightblue')

        #上盒
        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text="個人資料輸入:", style='topfra.TLabel').pack()
        topFrame.pack(expand=True,fill='x',padx=10,pady=(10,0))
        #end上盒

        #下盒
        bottomFrame = ttk.Frame(self)
        bottomFrame.columnconfigure(index= 0, weight=1)

        ttk.Label(bottomFrame, text="輸入帳號").grid(column= 0 ,row= 0,padx= 10,pady = 10)
        self.usn_entry=tk.StringVar()
        ttk.Entry(bottomFrame,textvariable=self.usn_entry).grid (column = 1,row = 0,padx= 10,pady = 10)

        ttk.Label(bottomFrame, text='輸入密碼').grid(column= 0, row= 1,padx= 10, pady= 10)
        self.pw_entry=tk.StringVar()
        ttk.Entry(bottomFrame,textvariable=self.pw_entry,show='@').grid(column= 1, row= 1,padx= 10, pady= 10)
        
        ok_btn = ttk.Button(bottomFrame,text='確定', command=self.ok_click)
        ok_btn.grid(column=0, row=3,padx=10,pady=(30,0))
        cancel_btn = ttk.Button(bottomFrame,text='取消',command=self.cancer_click)
        cancel_btn.grid(column=1,row=3,padx=10,pady=(30,0),sticky='E')

        bottomFrame.pack(expand=True,fill='x',padx= 10,pady= 10)
        #end下盒

    def cancer_click(self):
        self.usn_entry.set('')
        self.pw_entry.set('')

    def ok_click(self):
        username = self.usn_entry.get()
        password = self.pw_entry.get()
        showinfo(title="使用者輸入",message=f'使用者名稱:{username}\n使用者密碼:{password}')



        # bottombottomframe = ttk.Frame(self)
        # okbut = ttk.Button(bottombottomframe,text='確認')
        # okbut.pack(side='left')
        # canbut = ttk.Button(bottombottomframe,text='cancer')
        # canbut.pack(side='left')
        # bottombottomframe.pack()

        

def main():
    window = Window(theme="arc")
    # window.usn_entry.set("account")
    # window.pw_entry.set("password")
    window.mainloop()

if __name__ == '__main__':
    main()