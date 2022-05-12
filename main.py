import tkinter as tk
import cv2 as cv
from PIL import Image,ImageTk
from carID import *
from tkinter import Frame,filedialog
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        self.carmela_hight = 300
        self.carmela_width = 500
        self.Source_Img_Label = None
        self.Source_Img = None
        self.py_path = os.path.abspath(os.path.dirname(__file__))
        #初始化窗口
        Frame.__init__(self,master=master,bg="white")
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.window_init()
        #
        self.String_var = tk.StringVar()
        #
        self.createWidgets()

    def window_init(self):
        self.master.title('车牌识别综合实训')
        self.master.bg = 'white'
        width,height = (self.carmela_width,self.carmela_hight)
        self.master.geometry(f'{width}x{height}')

    def createWidgets(self):
        self.fm1 = Frame(self,bg='white')
        self.fm1_top = Frame(self.fm1)
        self.fm1_bottom = Frame(self.fm1)

        Img_Path_Text = tk.Entry(
            self.fm1_top,
            textvariable=self.String_var, 
            borderwidth=1, 
            state=tk.DISABLED)
        Img_Path_Text.pack(side='left')

        Img_Path_Button = tk.Button(
            self.fm1_top,
            text='选择',
            command=self.askPic())
    
        self.fm2 = Frame(self)
        self.Source_Img_Label = tk.Label(
            self.fm2,
            bg='white',
            image=None,
            width=200,
            height=200
        )
        self.Source_Img_Label.image = None
        self.Source_Img_Label.pack(side='right')
        self.fm2.pack(side=tk.LEFT)
    def CvtPIL(self,imgsrc):
        rgb_img = cv.cvtColor(imgsrc, cv.COLOR_BGR2RGB)
        rgb_img = Image.fromarray(rgb_img)
        rgb_img = ImageTk.PhotoImage(rgb_img)
        self.Source_Img_Label.configure(image=rgb_img)
        self.Source_Img_Label.image = rgb_img
    def askPic(self):
        Picture_Path = filedialog.askopenfilename()
        self.String_var.set(Picture_Path)
        self.Source_Img = cv.imread(Picture_Path)
        if (self.Source_Img is None):
            self.String_var.set('文件选择错误')
            return
        rgb_img = self.CvtPIL(self.Source_Img)

if __name__ == "__main__":
    win = Application()
    win.mainloop()