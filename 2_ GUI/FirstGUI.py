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

# Import the main GUI
import MainGUI

xTitle=320
yTitle=70
xSubtitle=270
ySubtitle=200
xentry1=420
yentry1=380
xentry2=500
yentry2=450
xSubmit=580
ySubmit=600


# Save paths to config file
def writeConfig(sofa_var, simul_var):

       # If config file exists go on
       if os.path.exists('Config.txt'):
              print("Config already exists")
       
       # If config file does not exist, create it
       else:
              # Create file and write on it   
              Config = open('Config.txt', 'x')
              Config = open('Config.txt', 'w')

              # Define data to write
              sofa=str(sofa_var.get())
              simul=str(simul_var.get())  

              var1 = f"{sofa}\n"
              var2 = f"{simul}"   

              # Write date on config file
              Config.write(var1)
              Config.write(var2)

              # Close file
              Config.close()

       callWin2()

# Call the other GUI
def callWin2():
       win2 = Toplevel(root)
       MainGUI.Window2(win2)


def Window1(win1):

       # Define window visual
       win1.geometry("1400x900")
       win1.configure(background='LightBlue1')

       # Entry variables
       sofa_var=tk.StringVar()
       simul_var=tk.StringVar()

       # Text
       label1 = tk.Label(win1, text='Prepare your computer:\nif you already did it, simply click submit')
       label1.config(font=('Arial', 30),background='LightBlue1')
       label1.place(x=xTitle-30, y=yTitle)


       # Text
       label2 = tk.Label(win1, text='Define here your paths to sofa and to the task simulations scripts.\nYou will need to do it once only.')
       label2.config(font=('Arial', 20),background='LightBlue1')
       label2.place(x=xSubtitle-30, y=ySubtitle)

       # Take lines in input: PATH TO SOFA
       sofa_path = tk.Label(win1, text = 'Insert your path to runSofa (for example: /build/v20.12.02/bin/Release)', font=('calibre',10, 'bold'))
       sofapath_entry = tk.Entry(win1, textvariable = sofa_var, font=('calibre',10,'normal'))
       sofa_path.place(x=xentry1, y=yentry1)
       sofapath_entry.place(x=xentry1+130, y=yentry1+20)
       sofa_path.configure(background='LightBlue1')
       #sofa_var.trace("w", writeConfig)

       # Take lines in input: PATH TO CODES
       simulations_path = tk.Label(win1, text = 'Insert your path to the medical simulations', font=('calibre', 10, 'bold'))
       simulations_entry = tk.Entry(win1,textvariable = simul_var, font=('calibre',10,'normal'))
       simulations_path.place(x=xentry2, y=yentry2)
       simulations_entry.place(x=xentry1+130, y=yentry2+20)
       simulations_path.configure(background='LightBlue1')
       #simul_var.trace("w", writeConfig)

       # Buttons
       submit_button = tk.Button(win1, text='Submit', command=partial(writeConfig,sofa_var,simul_var), bg='deepskyblue2', font=('Arial', 15, 'bold'))
       submit_button.place(x=xSubmit, y=ySubmit)



if __name__=="__main__":

    root = tk.Tk()
    Window1(root)
    root.mainloop()
