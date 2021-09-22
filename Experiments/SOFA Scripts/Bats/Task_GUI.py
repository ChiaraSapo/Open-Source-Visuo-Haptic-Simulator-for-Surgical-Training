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
       winFAM.geometry("1500x1000")
       winFAM.configure(background='LightBlue1')

       # Entry variable 
       user_var = tk.StringVar()

       # Text
       label1 = tk.Label(winFAM, text='SECONDA PARTE DEL TEST')
       label1.config(font=('Arial', 30))
       label1.place(x=xTitle, y=yTitle)
       label1.configure(background='LightBlue1')

       # Take lines in input: USER NAME
       LINE1 = tk.Label(winFAM, text = 'In questa parte del test verranno proposti tre tipi di esercizi guidati: ', font=('calibre', 15, 'bold'))
       LINE1.place(x=xentry, y=yentry, anchor='nw')
       LINE1.configure(background='LightBlue1')

       LINE1b = tk.Label(winFAM, text = 'incisione, manualità (passaggio attraverso degli anelli) e sutura', font=('calibre', 15, 'bold'))
       LINE1b.place(x=xentry, y=yentry+25, anchor='nw')
       LINE1b.configure(background='LightBlue1')

       LINE2 = tk.Label(winFAM, text = 'Per tutti i task è richiesto l utilizzo del Geomagic Touch della mano dominante.', font=('calibre', 15, 'bold'))
       LINE2.place(x=xentry2, y=yentry2, anchor='nw')
       LINE2.configure(background='LightBlue1')

       LINE2b = tk.Label(winFAM, text = 'Per l incisione: Tagliare lungo la linea visibile sulla pelle.', font=('calibre', 15, 'bold'))
       LINE2b.place(x=xentry2, y=yentry2+25, anchor='nw')
       LINE2b.configure(background='LightBlue1')

       LINE3 = tk.Label(winFAM, text = 'Per la manualità: Passare attraverso gli anelli senza toccarli, partendo da quello più lontano', font=('calibre', 15, 'bold'))
       LINE3.place(x=xentry3, y=yentry3, anchor='nw')
       LINE3.configure(background='LightBlue1')

       # Take lines in input: USER NAME
       LINE1 = tk.Label(winFAM, text = 'Per la sutura: Inserire l ago in corrispondenza delle sfereì colorate, procededendo quando diventano verdi.', font=('calibre', 15, 'bold'))
       LINE1.place(x=xentry3, y=yentry3+25, anchor='nw')
       LINE1.configure(background='LightBlue1')

       LINE1b = tk.Label(winFAM, text = 'e partendo dalla sfera più lontana. ', font=('calibre', 15, 'bold'))
       LINE1b.place(x=xentry4, y=yentry4, anchor='nw')
       LINE1b.configure(background='LightBlue1')

       LINE4 = tk.Label(winFAM, text = 'Se ci sono domande è possibile porle ora. Quando vuole inziare può premere HO CAPITO', font=('calibre', 15, 'bold'))
       LINE4.place(x=xentry4, y=yentry4+25, anchor='nw')
       LINE4.configure(background='LightBlue1')
       
              # Images
       image2 = Image.open("C:\sofa\src\Chiara\Bats\Images/cut.png")
       image2 = image2.resize((300, 200), Image.ANTIALIAS)
       image2 = ImageTk.PhotoImage(image2)
       label3 = tk.Label(winFAM, image=image2)
       label3.image = image2
       label3.place(x=xentry2+1000,y=yentry2-200)
       label3.configure(background='LightBlue1')

       # Images
       image1 = Image.open("C:\sofa\src\Chiara\Bats\Images/ring.png")
       image1 = image1.resize((300, 200), Image.ANTIALIAS)
       image1 = ImageTk.PhotoImage(image1)
       label2 = tk.Label(winFAM, image=image1)
       label2.image = image1
       label2.place(x=xentry2+1000,y=yentry2)
       label2.configure(background='LightBlue1')

       
              # Images
       image3 = Image.open("C:\sofa\src\Chiara\Bats\Images/sut.png")
       image3 = image3.resize((300, 200), Image.ANTIALIAS)
       image3 = ImageTk.PhotoImage(image3)
       label13 = tk.Label(winFAM, image=image3)
       label13.image = image3
       label13.place(x=xentry2+1000,y=yentry2+200)
       label13.configure(background='LightBlue1')

       # # Buttons
       submit_button = tk.Button(winFAM, text='HO CAPITO', command=partial(temp,winFAM), bg='lightskyblue2', font=('Arial', 15, 'bold'))
       submit_button.place(x=xSubmit, y=ySubmit)


       #os.system("start /wait cmd /c {command}")

if __name__ == "__main__":

    root = tk.Tk()
    WindowFAM(root)
    root.mainloop()
