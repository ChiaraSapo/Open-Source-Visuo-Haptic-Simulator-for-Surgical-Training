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


def write_bat(task_type, number_dev, dominant_hand): 
       Config=open('Config.txt')
       sofa=Config.readline()
       simul=Config.readline()
       Config.close()

       # Create bat file    
       if number_dev=='Single':
              bat_file_name=f'{task_type}_task_{dominant_hand}'
       else: 
              bat_file_name=f'{task_type}_task_{dominant_hand}_Double'      
       myBat = open(f'{bat_file_name}.bat', 'x')
       myBat = open(f'{bat_file_name}.bat', 'w')
       
       # Define commands to write
       command1 = f"cd {sofa}\n"
       command2 = f"runSofa {simul}\Single_Simulations\{bat_file_name}.py"

       # Write commands on the file
       myBat.write(command1)
       myBat.write(command2)

       # Close bat file
       myBat.close()


# Start suture simulation
def start_task(task_type, number_dev, dominant_hand): 
       
       number_dev="Single" # REMOVE THIS IF YOU ACTUALLY WANT TO USE A DOUBLE STATION: RIGHT NOW I WILL SET IT TO SINGLE
       if number_dev=='Single':
              bat_file_name=f'{task_type}_task_{dominant_hand}.bat'
       else: 
              bat_file_name=f'{task_type}_task_{dominant_hand}_Double.bat'

       if os.path.exists(bat_file_name): 
              print("File exists ")
              subprocess.call([bat_file_name])
              sys.exit()
       else:
              print("File does not exist")
              write_bat(task_type, number_dev, dominant_hand)

              time.sleep(6)
              subprocess.call([bat_file_name])
              sys.exit()





def writeUserFile(user_name,task_type,number_dev):
       
       if user_name=="":
              user_name="UnknownUser"
       fileName=f"{user_name}.txt"

       # Config = open('Config.txt', 'a')    
       # var=f"\n{user_name}"
       # Config.write(var)
       # Config.close()

       # Create/Open Data file
       if os.path.exists(fileName):
              Data = open(fileName, 'a')

       # Data does not exist: create file
       else:
              Data = open(fileName, 'x')
              Data = open(fileName, 'w')       
       
       # Take current time
       now = datetime.datetime.now()

       # Write interesting data on the Data file
       #var1 = f"\n\nDate: {now.day}/{now.month}/{now.year}\nTime: {now.hour}:{now.minute}\nTask type: {task_type}\nStation type: {number_dev}\n"
       var1 = f"\n\n{now.day}/{now.month}/{now.year}\n{now.hour}:{now.minute}\n{task_type}\n{number_dev}\n"

       # Write on Data
       Data.write(var1)

       # Close file
       Data.close()


# Define the medical task to be run
def run_medical_task(task_var,dev_n_var,user_var,dominant_hand_var,win2):
       
       # Get data
       task_type=str(task_var.get())
       number_dev=str(dev_n_var.get())
       user_name=str(user_var.get())
       dominant_hand=str(dominant_hand_var.get())

       writeUserFile(user_name,task_type,number_dev)
       start_task(task_type, number_dev, dominant_hand)




xTitle=320
yTitle=70
xImage=300
yImage=300
xentry=700
yentry=300
xoption1=700
yoption1=380
xoption2=700
yoption2=450
xoption3=700
yoption3=520
xSubmit=580
ySubmit=700

def Window2(win2):
       
       # Define window visual
       win2.geometry("1400x900")
       win2.configure(background='LightBlue1')

       # Option menus variables
       dev_n_var = tk.StringVar()
       task_var = tk.StringVar()
       plot_var = tk.StringVar()
       dominant_hand_var = tk.StringVar()

       # Entry variable 
       user_var = tk.StringVar()

       # Text
       label1 = tk.Label(win2, text='Run your SOFA Framework medical simulation')
       label1.config(font=('Arial', 30),background='LightBlue1')
       label1.place(x=xTitle-60, y=yTitle)

       # Images
       image1 = Image.open("Images\geo.png")
       image1 = image1.resize((200, 200), Image.ANTIALIAS)
       image1 = ImageTk.PhotoImage(image1)
       label2 = tk.Label(win2, image=image1)
       label2.image = image1
       label2.place(x=xImage,y=yImage)
       label2.configure(background='LightBlue1')

       # Take lines in input: USER NAME
       user_name = tk.Label(win2, text = 'Insert your name here', font=('calibre', 15, 'bold'))
       user_name_entry = tk.Entry(win2, textvariable = user_var, font=('calibre',10,'normal'))
       user_name.place(x=xentry, y=yentry, anchor='nw')
       user_name_entry.place(x=xentry+30, y=yentry+30, anchor='nw')
       user_name.configure(background='LightBlue1')
       
       # Option menus: TASKS
       task_options = ["Suture", "Incision", "Rings"]
       task_var.set("Select the medical task")
       question_menu2 = tk.OptionMenu(win2, task_var, *task_options)
       question_menu2.config(bg='skyblue1', font=('Arial', 15))
       question_menu2.pack()
       question_menu2.place(x=xoption1, y=yoption1, anchor='nw')
       question_menu2["menu"].config(bg="skyblue1", font=('Arial', 15))#, bd=0)
       #task_var.trace("w", run_medical_task)

       # Option menus: Number of devices
       dev_n_options = ["Single", "Double"]
       dev_n_var.set("Select the type of station")
       question_menu3 = tk.OptionMenu(win2, dev_n_var, *dev_n_options)
       question_menu3.config(bg='skyblue1', font=('Arial', 15))
       question_menu3.pack()
       question_menu3.place(x=xoption2, y=yoption2, anchor='nw')
       question_menu3["menu"].config(bg="skyblue1", font=('Arial', 15))#, bd=0)

       # Option menus: Dominant Hand
       hand_options = ["Right", "Left"]
       dominant_hand_var.set("Select your dominant hand")
       question_menu = tk.OptionMenu(win2, dominant_hand_var, *hand_options)
       question_menu.config(bg='skyblue1', font=('Arial', 15))
       question_menu.pack()
       question_menu.place(x=xoption2, y=yoption3, anchor='nw')
       question_menu["menu"].config(bg="skyblue1", font=('Arial', 15))#, bd=0)
       #dev_n_var.trace("w", run_medical_task)

       # Buttons
       submit_button = tk.Button(win2, text='Submit', command=partial(run_medical_task,task_var,dev_n_var,user_var,dominant_hand_var,win2), bg='skyblue1', font=('Arial', 15, 'bold'))
       submit_button.place(x=xSubmit, y=ySubmit)


       #os.system("start /wait cmd /c {command}")

if __name__ == "__main__":

    root = tk.Tk()
    Window2(root)
    root.mainloop()
