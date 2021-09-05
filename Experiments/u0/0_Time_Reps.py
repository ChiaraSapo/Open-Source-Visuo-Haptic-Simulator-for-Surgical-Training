import tkinter as tk
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np




ConfigName=open('Name.txt')
for line in ConfigName:
    pass
user_name = line
ConfigName.close()
print(user_name)


Time_length=np.empty(6)

for i in range(1,3):
    pos_name=f"Rep{i}_{user_name}_Incision2Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision2Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    temp=data_pos['Time']
    Time_length[i-1]=temp[temp.size-1]

for i in range(3,5):
    pos_name=f"Rep{i}_{user_name}_Incision3Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision3Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    
    temp=data_pos['Time']
    Time_length[i-1]=temp[temp.size-1]

for i in range(5,7):
    pos_name=f"Rep{i}_{user_name}_Incision4Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision4Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    temp=data_pos['Time']
    Time_length[i-1]=temp[temp.size-1]


fig = plt.figure(figsize=(20,10))
fig.suptitle('Incision repetitions time')
x=np.array(range(7))
plt.plot([1,2,3,4,5,6], Time_length,  color="darkturquoise", linewidth="2")
plt.xlabel('Repetitions')
plt.ylabel('Time[dt]')
plt.legend()
plt.xticks(x)
plt.grid()
#plt.show()


Time_length=np.empty(6)
count=0
for i in range(7,12):
    pos_name=f"Rep{i+1}_{user_name}_RingsPos_Double_x.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    temp=data_pos['Time']  
    Time_length[count]=temp[temp.size-1]
    count+=1



fig2 = plt.figure(figsize=(20,10))
fig2.suptitle('Rings repetitions time')
x=np.array(range(7))
plt.plot([1,2,3,4,5,6], Time_length,  color="darkturquoise", linewidth="2")
plt.xlabel('Repetitions')
plt.ylabel('Time[dt]')
plt.legend()
plt.xticks(x)
plt.grid()
#plt.show()


Time_length=np.empty(9)
count=0

for i in range(12,20):
    pos_name=f"Rep{i+1}_{user_name}_SuturePos_x.txt"
    vel_name=f"Rep{i+1}_{user_name}_SutureVel_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    temp=data_pos['Time']  
    Time_length[count]=temp[temp.size-1]
    count+=1



fig3 = plt.figure(figsize=(20,10))
fig3.suptitle('Suture repetitions time')
x=np.array(range(10))
plt.plot([1,2,3,4,5,6,7,8,9], Time_length,  color="darkturquoise", linewidth="2")
plt.xlabel('Repetitions')
plt.ylabel('Time[dt]')
plt.legend()
plt.xticks(x)
plt.grid()
#plt.show()


fig.savefig(f'Images\{user_name}_Incision_time_flow.png')
fig2.savefig(f'Images\{user_name}_Rings_time_flow.png')
fig3.savefig(f'Images\{user_name}_Suture_time_flow.png')