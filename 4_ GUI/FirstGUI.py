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

x1=400
x2=800
y1=200
y2=300
y3=500
x3=700
y4=600
y5=700

def toggle_fs(dummy=None):
    state = False if root.attributes('-fullscreen') else True
    root.attributes('-fullscreen', state)
    if not state:
        root.geometry('1000x800') 

def writeConfig():

    if os.path.exists('Config.txt'):
        root.destroy()
    else:
       # Create file and write on it   
       Config = open('Config.txt', 'x')
       Config = open('Config.txt', 'w')

       # Define commands to write
       sofa=str(sofa_var.get())
       simul=str(simul_var.get())  
       var1 = f"{sofa}\n"
       var2 = f"{simul}"   

       # Write commands
       Config.write(var1)
       Config.write(var2)

       # Close file
       Config.close()

       root.destroy()



root = tk.Tk() 
root.attributes('-fullscreen', True)
root.bind('<Escape>', toggle_fs)

sofa_var=tk.StringVar()
simul_var=tk.StringVar()
 
#canvas1 = tk.Canvas(root, width = 1000, height = 900) 
canvas1 = tk.Canvas(root, highlightthickness=0)
canvas1.pack(fill=tk.BOTH, expand=True)
canvas1.pack()

# Text
label1 = tk.Label(root, text='Define your variables')
#label1.config(anchor=CENTER, font=('Arial', 20))
#label1.pack()
label1.config(font=('Arial', 30))
canvas1.create_window(780, 100, window=label1)


# Buttons: make it rounded with https://stackoverflow.com/questions/42579927/rounded-button-tkinter-python
submit_button = tk.Button(root, text='Submit', command=writeConfig, bg='lightskyblue2', font=('Arial', 15, 'bold'))
canvas1.create_window(x3, y3, window=submit_button)
done_button = tk.Button(root, text='File already exists', command=root.destroy, bg='lightskyblue2', font=('Arial', 15, 'bold'))
canvas1.create_window(x3, y4, window=done_button)

sofa_path = tk.Label(root, text = 'Insert your path to runSofa (for example: /build/v20.12.02/bin/Release)', font=('calibre',10, 'bold'))
sofapath_entry = tk.Entry(root,textvariable = sofa_var, font=('calibre',10,'normal'))
sofa_path.place(x=x1, y=y1, anchor='nw')
sofapath_entry.place(x=x1, y=y1+30, anchor='nw')

simulations_path = tk.Label(root, text = 'Insert your path to the medical simulations', font=('calibre', 10, 'bold'))
simulations_entry = tk.Entry(root,textvariable = simul_var, font=('calibre',10,'normal'))
simulations_path.place(x=x1, y=y2, anchor='nw')
simulations_entry.place(x=x1, y=y2+30, anchor='nw')

root.mainloop()