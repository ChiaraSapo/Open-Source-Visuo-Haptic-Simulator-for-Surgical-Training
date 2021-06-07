#!/usr/bin/env python3
# https://datatofish.com/how-to-create-a-gui-in-python/ for more on GUIs on Tkinter

# Widget appearance https://flylib.com/books/en/2.723.1/configuring_widget_appearance.html 
# Colors http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

import subprocess
import tkinter as tk
from tkinter import *
import time
from PIL import ImageTk, Image  

x1=400
x2=800
y1=200
y2=500
y3=800
xm=700

def toggle_fs(dummy=None):
    state = False if root.attributes('-fullscreen') else True
    root.attributes('-fullscreen', state)
    if not state:
        root.geometry('1000x800') 


def start_suture(): 
       subprocess.call([r'D:\Thesis\run_suture.bat'])

def start_incision(): 
       subprocess.call([r'D:\Thesis\run_incision.bat'])

def run_medical_task():
       number_dev=str(dev_n_value.get())
       task_type=str(task_value.get())

       if task_type=="Incision":
              start_incision()
       elif task_type=="Suture":
              if number_dev=="1 haptic device":
                     start_suture()
              else:
                     print("2 devices simulation does not exist yet!")



root = tk.Tk() 
root.attributes('-fullscreen', True)
root.bind('<Escape>', toggle_fs)

dev_n_value = tk.StringVar(root)
task_value = tk.StringVar(root)

#canvas1 = tk.Canvas(root, width = 1000, height = 800) 
canvas1 = tk.Canvas(root, highlightthickness=0)
canvas1.pack(fill=tk.BOTH, expand=True)
canvas1.pack()

# Text
label1 = tk.Label(root, text='SOFA Framework medical simulation')
#label1.config(anchor=CENTER, font=('Arial', 20))
#label1.pack()
label1.config(font=('Arial', 30))
canvas1.create_window(780, 100, window=label1)


# Images
image1 = Image.open("D:\Thesis\Images\geo.png")
image1 = image1.resize((300, 300), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image1)

label2 = tk.Label(image=image1)
label2.image = image1
label2.place(x=x1,y=y1)

image2 = Image.open("D:\Thesis\Images\quokka.png")
image2 = image2.resize((200, 200), Image.ANTIALIAS)
image2 = ImageTk.PhotoImage(image2)

label3 = tk.Label(image=image2)
label3.image = image2
label3.place(x=x1,y=y2)


# Buttons: make it rounded with https://stackoverflow.com/questions/42579927/rounded-button-tkinter-python
submit_button = tk.Button(root, text='Submit', command=run_medical_task, bg='lightskyblue2', font=('Arial', 15, 'bold'))
canvas1.create_window(xm, y3, window=submit_button)

# Option menus
task_options = ["Suture", "Incision"]
task_value.set("Select the medical task")
question_menu2 = tk.OptionMenu(root, task_value, *task_options)
question_menu2.config(bg='skyblue1', font=('Arial', 15))
question_menu2.pack()
question_menu2.place(x=x2, y=y1+50, anchor='nw')
question_menu2["menu"].config(bg="skyblue1", font=('Arial', 15), bd=0)

dev_n_options = ["1 haptic device", "2 haptic devices"]
dev_n_value.set("Select the number of haptic devices")
question_menu = tk.OptionMenu(root, dev_n_value, *dev_n_options)
question_menu.config(bg='skyblue1', font=('Arial', 15))
question_menu.pack()
question_menu.place(x=x2, y=y2, anchor='nw')
question_menu["menu"].config(bg="skyblue1", font=('Arial', 15), bd=0)

root.mainloop()