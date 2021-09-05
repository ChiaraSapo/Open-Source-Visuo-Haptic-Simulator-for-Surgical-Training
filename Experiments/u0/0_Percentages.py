import tkinter as tk
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import collections  as mc
from matplotlib.patches import Rectangle

import numpy as np


ConfigName=open('Name.txt')
for line in ConfigName:
    pass
user_name = line
ConfigName.close()
print(user_name)

percentage= [0] * 20

for i in range(1,3):
    pos_name=f"Rep{i}_{user_name}_Incision2Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision2Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    temp=0
    posx=data_pos['x1']
    posy=data_pos['y1']

    for j in range(data_pos['Time'].size):
        if 6<= posx[j] <=8 and 10<= posy[j] <=22:
            temp+=1

    percentage[i-1]=temp*100/(posx.size)
    print(percentage[i-1])




for i in range(3,5):
    pos_name=f"Rep{i}_{user_name}_Incision3Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision3Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    temp=0
    posx=data_pos['x1']
    posy=data_pos['y1']

    for j in range(data_pos['Time'].size):
        if 6<= posx[j] <=8 and 10<= posy[j] <=22:
            temp+=1

    percentage[i-1]=temp*100/(posx.size)
    print(percentage[i-1])




for i in range(5,7):
    pos_name=f"Rep{i}_{user_name}_Incision4Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision4Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    temp=0
    posx=data_pos['x1']
    posy=data_pos['y1']

    for j in range(data_pos['Time'].size):
        if 6<= posx[j] <=8 and 10<= posy[j] <=22:
            temp+=1

    percentage[i-1]=temp*100/(posx.size)
    print(percentage[i-1])
  


count=1
for i in range(7,12):
    pos_name=f"Rep{i+1}_{user_name}_RingsPos_Double_x.txt"
    vel_name=f"Rep{i+1}_{user_name}_RingsVel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

  
count=1
for i in range(12,20):
    pos_name=f"Rep{i+1}_{user_name}_SuturePos_x.txt"
    vel_name=f"Rep{i+1}_{user_name}_SutureVel_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    #?subplot_name.plot(data_pos['x1'], data_pos['y1'],   color="palegreen", linewidth="2")

  