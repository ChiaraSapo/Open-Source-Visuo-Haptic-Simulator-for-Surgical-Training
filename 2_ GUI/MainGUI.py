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





# Write bat file to run the simulations
def writeBat(command=None):

       # Open config file, read it and then close it
       Config=open('Config.txt')
       sofa=Config.readline()
       simul=Config.readline()
       Config.close()

       # Create bat file 
       if command=="Suture_task.py":              
              myBat = open('run_suture.bat', 'x')
              myBat = open('run_suture.bat', 'w')
       elif command=="Incision_task.py":
              myBat = open('run_incision.bat', 'x')
              myBat = open('run_incision.bat', 'w')
       elif command=="Rings_task.py":
              myBat = open('run_rings.bat', 'x')
              myBat = open('run_rings.bat', 'w')
       
       # Define commands to write
       command1 = f"cd {sofa}\n"
       command2 = f"runSofa {simul}\{command}"

       # Write commands on the file
       myBat.write(command1)
       myBat.write(command2)

       # Close bat file
       myBat.close()


# Start suture simulation
def start_suture(): 
       try: 
              subprocess.call(['run_suture.bat'])
              sys.exit()
       except:
              writeBat("Suture_task.py")
              time.sleep(3)
              subprocess.call(['run_suture.bat'])
              sys.exit()

# Start suture simulation
def start_rings(): 
       try: 
              print("by bat")
              subprocess.call(['run_rings.bat'])
              sys.exit()
       except:
              writeBat("Rings_task.py")
              time.sleep(3)
              subprocess.call(['run_rings.bat'])
              sys.exit()


# Start incision simulation
def start_incision(): 
       try: 
              subprocess.call(['run_incision.bat'])
              sys.exit()
       except:
              writeBat("Incision_task.py")
              time.sleep(3)
              subprocess.call(['run_incision.bat'])
              sys.exit()

def writeUserFile(user_name,task_type,number_dev):
       
       if user_name=="":
              user_name="UnknownUser"
       fileName=f"{user_name}.txt"

       Config = open('Config.txt', 'a')    
       var=f"\n{user_name}"
       Config.write(var)
       Config.close()

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
def run_medical_task(task_var, dev_n_var, user_var, win2):
       
       # Get data
       task_type=str(task_var.get())
       number_dev=str(dev_n_var.get())
       user_name=str(user_var.get())

       writeUserFile(user_name,task_type,number_dev)
       
       if task_type=="Incision":
              if number_dev=="Single":
                     start_incision()
              elif number_dev=="Double":
                     print("Incision is only available with single station at the moment")
                     start_incision()

       elif task_type=="Suture":
              if number_dev=="Single":
                     start_suture()
              elif number_dev=="Double":
                     print("Suture is only available with single station at the moment")
                     start_suture()
       
       elif task_type=="Rings":
              if number_dev=="Single":
                     start_rings()
              elif number_dev=="Double":
                     print("Rings is only available with single station at the moment")
                     start_rings()



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
       hand_var = tk.StringVar()

       # Entry variable 
       user_var = tk.StringVar()

       # Text
       label1 = tk.Label(win2, text='Run your SOFA Framework medical simulation')
       label1.config(font=('Arial', 30),background='LightBlue1')
       label1.place(x=xTitle, y=yTitle)

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
       dev_n_options = ["One", "Two"]
       dev_n_var.set("Select the number of devices you have")
       question_menu3 = tk.OptionMenu(win2, dev_n_var, *dev_n_options)
       question_menu3.config(bg='skyblue1', font=('Arial', 15))
       question_menu3.pack()
       question_menu3.place(x=xoption2, y=yoption2, anchor='nw')
       question_menu3["menu"].config(bg="skyblue1", font=('Arial', 15))#, bd=0)

       # Option menus: Dominant Hand
       dev_n_options = ["Right", "Left"]
       hand_var.set("Select your dominant hand")
       question_menu = tk.OptionMenu(win2, hand_var, *dev_n_options)
       question_menu.config(bg='skyblue1', font=('Arial', 15))
       question_menu.pack()
       question_menu.place(x=xoption2, y=yoption3, anchor='nw')
       question_menu["menu"].config(bg="skyblue1", font=('Arial', 15))#, bd=0)
       #dev_n_var.trace("w", run_medical_task)

       # # Option menus: Number of devices
       # plot_options = ["Plot pos/vel/acc/force/traj", "Plot trajectory only", "Plot nothing"]
       # plot_var.set("Select the desired plots")
       # question_menu3 = tk.OptionMenu(win2, plot_var, *plot_options)
       # question_menu3.config(bg='skyblue1', font=('Arial', 15))
       # question_menu3.pack()
       # question_menu3.place(x=xoption3, y=yoption3, anchor='nw')
       # question_menu3["menu"].config(bg="skyblue1", font=('Arial', 15), bd=0)

       # Buttons
       submit_button = tk.Button(win2, text='Submit', command=partial(run_medical_task,task_var,dev_n_var,user_var,win2), bg='skyblue1', font=('Arial', 15, 'bold'))
       submit_button.place(x=xSubmit, y=ySubmit)


       #os.system("start /wait cmd /c {command}")

if __name__ == "__main__":

    root = tk.Tk()
    Window2(root)
    root.mainloop()
