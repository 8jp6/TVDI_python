from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        style = ttk.Style(self)
        style.configure("fontmid.TButton",anchor = "center")


        #上框
        topFrame = ttk.Frame(self,borderwidth=1,relief='groove')
        btn1 = ttk.Button(topFrame,text="按鈕1",style="fontmid.TButton")
        btn1.pack(side='left',expand=True,fill='x',padx=10)
        btn2 = ttk.Button(topFrame,text="按鈕2",style="fontmid.TButton")
        btn2.pack(side='left',expand=True,fill='x')
        btn3 = ttk.Button(topFrame,text="按鈕3",style="fontmid.TButton")
        btn3.pack(side='left',expand=True,fill='x',padx=10)
        topFrame.pack(padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='x')

        #下框
        bottomFrame = ttk.Frame(self,width=500,height=300,borderwidth=1,relief='groove')
        bottomFrame.pack(padx=10,pady=10)

        #下左框
        leftbottomFrame1 = ttk.Frame(bottomFrame,width = 160, height=300,borderwidth=1,relief="groove")
        bottomleftbtn1 = ttk.Button(leftbottomFrame1,text="按鈕4",style="fontmid.TButton")
        bottomleftbtn1.pack(expand=True,fill='y',padx=10,pady=5,ipady=40)
        bottomleftbtn2 = ttk.Button(leftbottomFrame1,text="按鈕5",style="fontmid.TButton")
        bottomleftbtn2.pack(expand=True,fill='y',padx=10,ipady=15)
        bottomleftbtn3 = ttk.Button(leftbottomFrame1,text="按鈕6",style="fontmid.TButton")
        bottomleftbtn3.pack(expand=True,fill='y',padx=10,pady=5,ipady=15)
        leftbottomFrame1.pack(padx=10,pady=10,side="left")
        
        #下中框
        bottombottomFrame2 = ttk.Frame(bottomFrame,width = 160, height=300,borderwidth=1,relief="groove")
        bottommidbtn1 = ttk.Button(bottombottomFrame2,text="按鈕7",style="fontmid.TButton")
        bottommidbtn1.pack(expand=True,fill='y',padx=10,pady=5,ipady=30)
        bottommidbtn2 = ttk.Button(bottombottomFrame2,text="按鈕8",style="fontmid.TButton")
        bottommidbtn2.pack(expand=True,fill='y',padx=10,ipady=10)
        bottommidbtn3 = ttk.Button(bottombottomFrame2,text="按鈕9",style="fontmid.TButton")
        bottommidbtn3.pack(expand=True,fill='y',padx=10,pady=5,ipady=30)
        bottombottomFrame2.pack(padx=10,pady=10,side="left")
        #下右框
        rightbottomFrame3 = ttk.Frame(bottomFrame,width = 160, height=300,borderwidth=1,relief="groove")
        bottomrightbtn1 = ttk.Button(rightbottomFrame3,text="按鈕10",style="fontmid.TButton")
        bottomrightbtn1.pack(expand=True,fill='y',padx=10,pady=5,ipady=23.3)
        bottomrightbtn2 = ttk.Button(rightbottomFrame3,text="按鈕11",style="fontmid.TButton")
        bottomrightbtn2.pack(expand=True,fill='y',padx=10,ipady=23.3)
        bottomrightbtn3 = ttk.Button(rightbottomFrame3,text="按鈕12",style="fontmid.TButton")
        bottomrightbtn3.pack(expand=True,fill='y',padx=10,pady=5,ipady=23.3)
        rightbottomFrame3.pack(padx=10,pady=10,side="left")


def main():
    window = Window(theme="black")
    window.mainloop()

if __name__ == '__main__':
    main()