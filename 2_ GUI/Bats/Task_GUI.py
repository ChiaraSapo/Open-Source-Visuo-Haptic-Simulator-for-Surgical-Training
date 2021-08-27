#!/usr/bin/env python3
# https://datatofish.com/how-to-create-a-gui-in-python/ for more on GUIs on Tkinter

# Widget appearance https://flylib.com/books/en/2.723.1/configuring_widget_appearance.html 
# Colors http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

import subprocess
import tkinter as tk
from tkinter import *
import time
from PIL import ImageTk, Image  
import os
from functools import partial
import datetime
import sys







xTitle=300
yTitle=70
xentry=80
yentry=300
xentry2=80
yentry2=350
xentry3=80
yentry3=400
xentry4=80
yentry4=450
xSubmit=500
ySubmit=600

def temp(winFAM):
       print("OK")
       winFAM.destroy()


def WindowFAM(winFAM):
       
       # Define window visual
       winFAM.geometry("1400x900")
       winFAM.configure(background='LightBlue1')

       # Entry variable 
       user_var = tk.StringVar()

       # Text
       label1 = tk.Label(winFAM, text='SECONDA PARTE DEL TEST')
       label1.config(font=('Arial', 30))
       label1.place(x=xTitle, y=yTitle)
       label1.configure(background='LightBlue1')

       # Take lines in input: USER NAME
       LINE1 = tk.Label(winFAM, text = 'In questa parte del test verranno proposti all utente tre tipi di esercizi guidati: incisione, manualità e sutura', font=('calibre', 15, 'bold'))
       LINE1.place(x=xentry, y=yentry, anchor='nw')
       LINE1.configure(background='LightBlue1')

       LINE1b = tk.Label(winFAM, text = 'incisione, manualità e sutura', font=('calibre', 15, 'bold'))
       LINE1b.place(x=xentry, y=yentry+25, anchor='nw')
       LINE1b.configure(background='LightBlue1')

       LINE2 = tk.Label(winFAM, text = 'Per il task di incisione è richiesto l utilizzo del Geomagic Touch di destra, ', font=('calibre', 15, 'bold'))
       LINE2.place(x=xentry2, y=yentry2, anchor='nw')
       LINE2.configure(background='LightBlue1')

       LINE2b = tk.Label(winFAM, text = 'mentre per il task di manualità e sutura si possono utilizare entrambi gli strumenti', font=('calibre', 15, 'bold'))
       LINE2b.place(x=xentry2, y=yentry2+25, anchor='nw')
       LINE2b.configure(background='LightBlue1')

       LINE3 = tk.Label(winFAM, text = 'Per passare l ago da uno strumento all altro si devono avvicinare le estremità dei due strumenti', font=('calibre', 15, 'bold'))
       LINE3.place(x=xentry3, y=yentry3, anchor='nw')
       LINE3.configure(background='LightBlue1')

       LINE3b = tk.Label(winFAM, text = 'e premere uno dei bottoni posti sul device di sinistra', font=('calibre', 15, 'bold'))
       LINE3b.place(x=xentry3, y=yentry3+25, anchor='nw')
       LINE3b.configure(background='LightBlue1')

       LINE4 = tk.Label(winFAM, text = 'Se hai domande chiedi ora, e quando vuoi iniziare premi HO CAPITO', font=('calibre', 15, 'bold'))
       LINE4.place(x=xentry4, y=yentry4, anchor='nw')
       LINE4.configure(background='LightBlue1')

       # # Buttons
       submit_button = tk.Button(winFAM, text='HO CAPITO', command=partial(temp,winFAM), bg='lightskyblue2', font=('Arial', 15, 'bold'))
       submit_button.place(x=xSubmit, y=ySubmit)


       #os.system("start /wait cmd /c {command}")

if __name__ == "__main__":

    root = tk.Tk()
    WindowFAM(root)
    root.mainloop()
