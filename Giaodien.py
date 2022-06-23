from random import sample
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter 
from threading import Thread
import cv2
import PIL.Image,PIL.ImageTk
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import model_from_json,load_model
from tensorflow.keras.optimizers import SGD
from keras.preprocessing.image import load_img,img_to_array
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfilename
import customtkinter
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.preprocessing import image


list_name = ['0', 'BENIGOI', 'CHAGOI', 'GOMO', 'HI_UTS ', 'HIKARIMOYO', 'KIKUSUI', 'SHOWA', 'SHUSHUI', 'TANCHO', 'UTSU_KI', 'UTS_SHIRO', 'ASAGI', 'BEKKO', 'GOSHIKI', 'KOHAKU', 'KUMONRYU', 'OCHIBA', 'SANKE']
model=load_model("cakoi.h5")
isOn = 0



def compare():
    global sample
    global frame
    global pos
    global canvas, photo
    global ret
    roi = frame
    if ret == False:
        return
    img = cv2.resize(roi,(128,128))
    img = img.reshape(1,128,128,3)
    img = img.astype('float32')
    img = img/255.0
    pos = int(np.argmax(model.predict(img)))
    patio = np.max(model.predict(img))*100
    patio = round(patio,4)
    print(list_name[pos])
    
def movideo():
    global file
    global video
    global canvas,photo
    global ret,frame, pos
    global isOn
    file = askopenfilename(filetypes=(("Video files", " *.mp4;*.flv;*.avi;*.mkv"),("All files", "*.*") ))
    video = cv2.VideoCapture(file)
    canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    canvas.config(width=canvas_w,height=canvas_h)
    print(file)
    ret,frame = video.read()
    frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
    canvas.create_image(0,0,image=photo,anchor=tkinter.NW) 
    video = cv2.VideoCapture(file) 

def onOpenCamera():
    global file
    global video
    global canvas,photo
    global ret,frame, pos
    global isOn
    video = cv2.VideoCapture(0)    
    canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    canvas.config(width=canvas_w,height=canvas_h)

def moanh():
    global file
    global video
    global canvas,photo
    global ret,frame, pos
    global isOn
    file = askopenfilename(filetypes=(("Picture file", "*.jpg; *.png"),("All files", "*.*") ))
    plt.imshow(file)
    canvas.config(width=128,height=128)

    
def Nhandien():
    global isOn
    isOn=2
    isOn=1
    print(isOn)

def Nhandienanh():
    global isOn
    isOn=3

def onStop():
    global isOn
    isOn=0

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = Tk()
root.title('----------------NHẬN DIỆN CÁ KOI --------------')
root.geometry("1800x1000")



label1 = Label(text='',font=("Arial", 70 ))
label1.place(x=800,y=60)
 
BUVIDEO = customtkinter.CTkButton(root,text="CHỌN VIDEO",command=movideo)
BUVIDEO.place(x=100,y=10,  width=120, height=40 )

BUNHAN = customtkinter.CTkButton(root,text="NHẬN DIỆN",command=Nhandien)
BUNHAN.place(x=175 ,y=60, width=120, height=40)

BUREAL =customtkinter.CTkButton(root,text="REAL TIME",command=onOpenCamera)
BUREAL.place(x=250,y=10,width=120, height=40)

BUANH= customtkinter.CTkButton(root,text="CHỌN ẢNH",command=moanh)
BUANH.place(x=400,y=10,  width=120, height=40 )

Nhandienanh = customtkinter.CTkButton(root,text="NHẬN DIỆN ẢNH",command=Nhandienanh)
Nhandienanh.place(x=400 ,y=60, width=120, height=40)


btnOn = customtkinter.CTkButton(root,text="STOP",command=onStop)
btnOn.place(x=600,y=10, width=120, height= 100)



pos=0
canvas = Canvas(root)
canvas.place(x=30,y=150)

def update_frame():
    global canvas,photo
    global ret,frame, pos
    global isOn
    global image,video

    if isOn == 1:
        ret,frame = video.read()
        if ret == False:
            isOn=0
            root.after(200,update_frame)
            return
        frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        thread = Thread(target=compare)
        thread.start()
        label1.config(text=list_name[pos],font=("Arial", 30))
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
        canvas.create_image(0,0,image=photo,anchor=tkinter.NW)
        
    if isOn == 2:
        ret,frame = video.read()
        if ret == False:
            isOn=0
            root.after(200,update_frame)
            return
        frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame1 = cv2.flip(frame1, 1)
        thread = Thread(target=compare)
        thread.start()
        label1.config(text=list_name[pos],font=("Arial", 30))
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
        canvas.create_image(0,0,image=photo,anchor=tkinter.NW)
    
    if isOn == 3:
        plt.imshow()
        pic = img_to_array(pic)
        pic = pic.reshape(1,128,128,3) 
        pic = pic.astype('float32')
        pic = pic/255
        thread = Thread(target=compare)
        thread.start()
        label1.config(text=list_name[pos],font=("Arial", 30))
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
        canvas.create_image(0,0,image=photo,anchor=tkinter.NW)


    root.after(200,update_frame)

update_frame()
root.mainloop()
