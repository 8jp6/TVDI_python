from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        style = ttk.Style(self)     
        #上框   
        topFrame = ttk.Frame(self,borderwidth=1,relief='groove')

        btn1 = ttk.Button(topFrame,text="按鈕1")
        btn1.pack(side='left',expand=True,fill='x',padx=10)
        btn2 = ttk.Button(topFrame,text="按鈕2")
        btn2.pack(side='left',expand=True,fill='x')
        btn3 = ttk.Button(topFrame,text="按鈕3")
        btn3.pack(side='left',expand=True,fill='x',padx=10)

        topFrame.pack(padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='x')
        #上框
        #下框
        bottomFrame = ttk.Frame(self,width=500,height=300,borderwidth=1,relief='groove')
        bottombottomFrame1 = ttk.Frame(bottomFrame,width = 160, height=300,borderwidth=1,relief="groove")
        # bottomleftbtn1 = ttk.Button(bottomFrame,text="按鈕4")
        # bottomleftbtn1.pack(side='left',expand=True,fill='y',padx=10)
        # bottomleftbtn2 = ttk.Button(bottomFrame,text="按鈕5")
        # bottomleftbtn2.pack(side='left',expand=True,fill='y',padx=10)
        # bottomleftbtn3 = ttk.Button(bottomFrame,text="按鈕6")
        # bottomleftbtn3.pack(side='left',expand=True,fill='y',padx=10)
        bottombottomFrame1.pack(padx=10,pady=10)

        bottombottomFrame2 = ttk.Frame(bottomFrame,width = 160, height=300,borderwidth=1,relief="groove")

        bottombottomFrame2.pack(padx=10,pady=10)

        bottombottomFrame3 = ttk.Frame(bottomFrame,width = 160, height=300,borderwidth=1,relief="groove")
        
        bottombottomFrame3.pack(padx=10,pady=10)

        bottomFrame.pack(padx=10,pady=10)
        #下框






def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()