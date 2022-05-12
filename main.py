import tkinter as tk
import cv2 as cv
from PIL import Image
def changeLabelImage(labelSrc,imageSrc):
    img = cv.cvtColor(imageSrc, cv.COLOR_BGR2RGB)
    rgbImage = Image.fromarray(img)
    resizeImg = 

def createWindow():
    bg = '#0fee0f'
    win = tk.Tk()
    win.title('车牌综合程序')
    win.geometry('300x300')
    win.configure(bg=bg)

    box=tk.Frame(width=100, height=25, borderwidth=0, bg=bg)
    box.grid(row=0,column=0,padx=20,pady=10)
    
    lblchepai = tk.Label(box,text='选择车牌',bg=bg)
    lblchepai.grid(row=0,column=0,padx=10,pady=5)

    win.mainloop()
if __name__ == "__main__":
    main()