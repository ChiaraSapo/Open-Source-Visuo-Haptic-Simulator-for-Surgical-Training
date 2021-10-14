#!/usr/bin/env python3
# https://datatofish.com/how-to-create-a-gui-in-python/ for more on GUIs on Tkinter

# Widget appearance https://flylib.com/books/en/2.723.1/configuring_widget_appearance.html 
# Colors http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

import subprocess
import tkinter as tk
from tkinter import *
import time
import os
import sys



simul_path="C:\sofa\src\Chiara"
sofa_path="C:\sofa\build\v20.12.02\bin\Release"
task_list=[# Single, right
"Suture_task_Right", 
"Incision_task1_Right", "Incision_task2_Right", "Incision_task3_Right",
"Rings_task_Right",
# Single, left
"Suture_task_Left", 
"Incision_task1_Left", "Incision_task2_Left", "Incision_task3_Left",
"Rings_task_Left",
# Double, right
"Suture_task_Right_Double", 
"Incision_task1_Right_Double", "Incision_Right_task2_Double", "Incision_Right_task3_Double",
"Rings_task_Right_Double",
# Double, left
"Suture_task_Left_Double", 
"Incision_task1_Left_Double", "Incision_task2_Left_Double", "Incision_task3_Left_Double",
"Rings_task_Left_Double"]

for task in task_list:             
       myBat = open(f'{task}.bat', 'x')
       myBat = open(f'{task}.bat', 'w')

       # Define commands to write
       command1 = f"cd {sofa_path}\n"
       command2 = f"runSofa {simul_path}\{task}.py -a"

       # Write commands on the file
       myBat.write(command1)
       myBat.write(command2)

       # Close bat file
       myBat.close()

