import os, tkinter, cv2
from turtle import color, width
import numpy as np 
from PIL import Image,ImageTk
from tkinter import filedialog, Frame

from carID import *
from pandas import wide_to_long

背景 = '#a0ffa0'
class Application(Frame):
    def __init__(self,master = None):
        self.carmela_hight = 600
        self.carmela_width = 600
        self.Source_Img_Label = None
        self.Source_Img = None
        self.py_path = os.path.abspath(os.path.dirname(__file__))
        Frame.__init__(self,master,bg = 背景)
        self.pack(expand= tkinter.YES, fill=tkinter.BOTH)
        self.window_init()
        self.String_var = tkinter.StringVar() 
        self.createWidgets()
    def window_init(self):
        self.master.title('滤镜')
        self.master.bg = '#a0ffa0'
        width, height = (self.carmela_width,self.carmela_hight)
        self.master.geometry(f"{width}x{height}")

    def createWidgets(self):
        self.fml = Frame(self,bg = 背景)
        self.fml_top = Frame(self.fml)
        self.fml_bottom = Frame(self.fml)
        Img_Path_Text = tkinter.Entry(self.fml_top,textvariable=self.String_var,borderwidth=1,state=tkinter.DISABLED)
        Img_Path_Text.pack(side='left')
        Img_Path_Button = tkinter.Button(self.fml_top,text='选择',command=self.AskPicture)
        Img_Path_Button.pack(side='right')
        # Outline_Button = tkinter.Button(self.fml_bottom,text='轮廓',command=self.OutlinePicture)
        # Outline_Button.pack(side='left')
        # Sharpen_Button = tkinter.Button(self.fml_bottom,text='锐化',command=self.SharpenPicture)
        # Sharpen_Button.pack(side='left')
        # Emboss_Button = tkinter.Button(self.fml_bottom,text='浮雕',command=self.EmbossPicture)
        # Emboss_Button.pack(side='left')

        pickOut_Buttom = tkinter.Button(
            self.fml_bottom,
            text='识别',
            command=self.pickOut
        )
        pickOut_Buttom.pack(side='left')

        self.fml_top.pack(side=tkinter.TOP)
        self.fml_bottom.pack(side=tkinter.BOTTOM)
        self.fml.pack(side=tkinter.LEFT)

        self.fm2 = Frame(self)
        self.Source_Img_Label = tkinter.Label(self.fm2, bg= 背景 , image=None, width=200, height=200)
        self.Source_Img_Label.image=None
        self.Source_Img_Label.pack(side='right')
        self.fm2.pack(side=tkinter.LEFT)
        
    def CvtPIL(self,srcImg):
        Rgb_Img = cv2.cvtColor(srcImg, cv2.COLOR_BGR2RGB)
        # Rgb_Img = cv2.resize(Rgb_Img,(100,100))
        Rgb_Img = Image.fromarray(Rgb_Img)
        Rgb_Img = ImageTk.PhotoImage(Rgb_Img)
        
        self.Source_Img_Label.configure(image=Rgb_Img)
        self.Source_Img_Label.image = Rgb_Img

    def AskPicture(self):
        Picture_Path = filedialog.askopenfilename()
        self.String_var.set(Picture_Path)
        self.Source_Img = cv2.imread(Picture_Path)
        if (self.Source_Img is None):
            self.String_var.set('文件选择错误')
            return
        self.CvtPIL(self.Source_Img)
    
    def pickOut(self):
        if (self.Source_Img is None):
            self.String_var.set('文件选择错误')
            return     
        self.String_var.set(carID(self.Source_Img,'./src'))
    # def OutlinePicture(self):
    #     if (self.Source_Img is None):
    #         self.String_var.set('文件选择错误')
    #         return
    #     kernel = np.array((
    #         [-1,-1,-1],
    #         [-1,8,-1],
    #         [-1,-1,-1]),dtype = 'float32')
    #     dstimg = cv2.filter2D(self.Source_Img, -1, kernel=kernel)
    #     self.CvtPIL(dstimg)
    # def SharpenPicture(self):
    #     if (self.Source_Img is None):
    #         self.String_var.set('文件选择错误')
    #         return
    #     kernel = np.array((
    #         [-2,-1,0],
    #         [-1,1,1],
    #         [0,1,2]),dtype = 'float32')
    #     dstimg = cv2.filter2D(self.Source_Img, -1, kernel=kernel)
    #     self.CvtPIL(dstimg)
    # def EmbossPicture(self):
    #     if (self.Source_Img is None):
    #         self.String_var.set('文件选择错误')
    #         return
    #     kernel = np.array((
    #         [-1,-1,-1],
    #         [-1,9,-1],
    #         [-1,-1,-1]),dtype = 'float32')
    #     dstimg = cv2.filter2D(self.Source_Img, -1, kernel=kernel)
    #     self.CvtPIL(dstimg)

if __name__ == '__main__':
    app = Application()
    app.mainloop()