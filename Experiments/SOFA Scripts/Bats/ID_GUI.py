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




def writeUserFile(user_var,win2):

       user_name=str(user_var.get())
       
       
       if user_name=="":
              print("ERROR!")

       # Create/Open Data file
       if os.path.exists('Config.txt'):
              Data = open('Config.txt', 'a')  

       # Data does not exist: create file
       else:
              Data = open('Config.txt', 'x')
              Data = open('Config.txt', 'w')       
       
       # Take current time
       now = datetime.datetime.now()

       # Write interesting data on the Data file
       var1 = f"\n\n{now.day}/{now.month}/{now.year}\n{now.hour}:{now.minute}\n{user_name}"

       # Write on Data
       Data.write(var1)

       # Close file
       Data.close()

       win2.destroy()



xTitle=320
yTitle=70
xentry=700
yentry=300
xSubmit=580
ySubmit=700

def Window2(win2):
       
       # Define window visual
       win2.geometry("1500x1000")
       win2.configure(background='LightBlue1')

       # Entry variable 
       user_var = tk.StringVar()

       # Text
       label1 = tk.Label(win2, text='Buongiorno, sta per incominciare l esperimento')
       label1.config(font=('Arial', 30))
       label1.place(x=xTitle, y=yTitle+40)
       label1.configure(background='LightBlue1')

       # Take lines in input: USER NAME
       user_name = tk.Label(win2, text = 'Inserire ID utente', font=('calibre', 15, 'bold'))
       user_name_entry = tk.Entry(win2, textvariable = user_var, font=('calibre',10,'normal'))
       user_name.place(x=xentry-45, y=yentry, anchor='nw')
       user_name_entry.place(x=xentry-40, y=yentry+30, anchor='nw')    
       user_name.configure(background='LightBlue1')
     
       # Buttons
       submit_button = tk.Button(win2, text='Submit', command=partial(writeUserFile,user_var,win2), bg='lightskyblue2', font=('Arial', 15, 'bold'))
       submit_button.place(x=xentry-15, y=yentry+200)


       #os.system("start /wait cmd /c {command}")

if __name__ == "__main__":

    root = tk.Tk()
    Window2(root)
    root.mainloop()
