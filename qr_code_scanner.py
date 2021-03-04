from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox, filedialog
from pyzbar.pyzbar import decode, ZBarSymbol
import cv2
import pyautogui
import numpy as np
import threading
from PIL import Image, ImageTk, ImageDraw
import os
 

 def scann(self,font_video=0):
    self.active_camera = False
    self.info = []
    self.codelist = []
    self.appName = 'QR Code Reader'
    self.ventana = Toplevel()
    self.ventana.title(self.appName)
    self.ventana['bg']='black'
    self.font_video=font_video
    self.label=Label(self.ventana,text=self.appName,font=15,bg='blue',
                        fg='white').pack(side=TOP,fill=BOTH)

    self.display=scrolledtext.ScrolledText(self.ventana,width=86,background='snow3'
                                    ,height=4,padx=10, pady=10,font=('Arial', 10))
    self.display.pack(side=BOTTOM)
    self.active_cam()
    
def active_cam(self):
    if self.active_camera == False:
        self.active_camera = True
        self.VideoCaptura()
        self.visor()
    else:
        self.active_camera = False
        self.codelist = []
        self.btnCamera.configure(text="INICIAR LECTURA POR CAMARA")
        self.vid.release()
        self.canvas.delete('all')
        self.canvas.configure(height=0)
