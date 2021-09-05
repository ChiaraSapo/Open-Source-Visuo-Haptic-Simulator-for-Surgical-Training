import tkinter as tk
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import collections  as mc


ConfigName=open('Name.txt')
for line in ConfigName:
    pass
user_name = line
ConfigName.close()
print(user_name)




fig = plt.figure(figsize=(20,10))
fig.suptitle('Incision 2D trajectory')

x_lines1=[0,14]
y_lines1=[10,10]

x_lines2=[0,14]
y_lines2=[22,22]

x_lines3=[0,0]
y_lines3=[10,22]

x_lines4=[7,7]
y_lines4=[10,22]

x_lines5=[ 14,14]
y_lines5=[ 10,22]

for i in range(1,3):
    pos_name=f"Rep{i}_{user_name}_Incision2Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision2Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    
    plt.subplot(2,3,i)
    
    plt.plot(x_lines1, y_lines1, color="pink", lw=2)
    plt.plot(x_lines2, y_lines2, color="pink", lw=2)
    plt.plot(x_lines3, y_lines3, color="pink", lw=2)
    plt.plot(x_lines4, y_lines4, color="pink", lw=2)
    plt.plot(x_lines5, y_lines5, color="pink", lw=2)
    plt.plot(data_pos['x1'], data_pos['y1'],   color="salmon", linewidth="2")
    plt.xlabel('x[cm]')
    plt.ylabel('y[cm]')
    plt.xlim([-1,15])
    plt.ylim([8,25])
    plt.legend()
    plt.grid()

for i in range(3,5):
    pos_name=f"Rep{i}_{user_name}_Incision3Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision3Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    plt.subplot(2,3,i)
    
    plt.plot(x_lines1, y_lines1, color="pink", lw=2)
    plt.plot(x_lines2, y_lines2, color="pink", lw=2)
    plt.plot(x_lines3, y_lines3, color="pink", lw=2)
    plt.plot(x_lines4, y_lines4, color="pink", lw=2)
    plt.plot(x_lines5, y_lines5, color="pink", lw=2)
    plt.plot(data_pos['x1'], data_pos['y1'],   color="salmon", linewidth="2")
    plt.xlabel('x[cm]')
    plt.ylabel('y[cm]')
    plt.xlim([-1,15])
    plt.ylim([8,25])
    plt.legend()
    plt.grid()



for i in range(5,7):
    pos_name=f"Rep{i}_{user_name}_Incision4Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision4Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    plt.subplot(2,3,i)
    plt.plot(x_lines1, y_lines1, color="pink", lw=2)
    plt.plot(x_lines2, y_lines2, color="pink", lw=2)
    plt.plot(x_lines3, y_lines3, color="pink", lw=2)
    plt.plot(x_lines4, y_lines4, color="pink", lw=2)
    plt.plot(x_lines5, y_lines5, color="pink", lw=2)
    plt.plot(data_pos['x1'], data_pos['y1'],   color="salmon", linewidth="2")
    plt.xlabel('x[cm]')
    plt.ylabel('y[cm]')
    plt.xlim([-1,15])
    plt.ylim([8,25])
    plt.legend()
    plt.grid()

#plt.show()


fig2 = plt.figure(figsize=(20,10))
fig2.suptitle('Rings 2D trajectory')

x_rings=[7,7,13,13]
y_rings=[5,13,8.5,15.5]

x_lines1=[0,10]
y_lines1=[0,0]

x_lines2=[0,0]
y_lines2=[0,20]

x_lines3=[0,10]
y_lines3=[20,20]

x_lines4=[10,10]
y_lines4=[0,20]


x_lines12=[11,22]
y_lines12=[0,0]

x_lines22=[11,11]
y_lines22=[0,20]

x_lines32=[11,22]
y_lines32=[20,20]

x_lines42=[22,22]
y_lines42=[0,20]


count=1
for i in range(7,12):
    pos_name=f"Rep{i+1}_{user_name}_RingsPos_Double_x.txt"
    vel_name=f"Rep{i+1}_{user_name}_RingsVel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    plt.subplot(2,3,count)
    
    plt.plot(x_lines1, y_lines1, color="pink", lw=2)
    plt.plot(x_lines2, y_lines2, color="pink", lw=2)
    plt.plot(x_lines3, y_lines3, color="pink", lw=2)
    plt.plot(x_lines4, y_lines4, color="pink", lw=2)
    plt.plot(x_lines12, y_lines12, color="pink", lw=2)
    plt.plot(x_lines22, y_lines22, color="pink", lw=2)
    plt.plot(x_lines32, y_lines32, color="pink", lw=2)
    plt.plot(x_lines42, y_lines42, color="pink", lw=2)
    plt.plot(data_pos['x1'], data_pos['y1'],   color="salmon", linewidth="2",zorder=1)
    plt.scatter(x_rings, y_rings, s=100, color="green",zorder=2)
    plt.xlabel('x[cm]')
    plt.ylabel('y[cm]')
    plt.legend()
    plt.grid()
    count+=1
#plt.show()


x_spheres=[8,8,13.5,13.5]
y_spheres=[4,10,4.5,10.5]

x_lines1=[0,10]
y_lines1=[0,0]

x_lines2=[0,0]
y_lines2=[0,16.5]

x_lines3=[0,10]
y_lines3=[16.5,16.5]

x_lines4=[10,10]
y_lines4=[0,16.5]


x_lines12=[10.5,21]
y_lines12=[0,0]

x_lines22=[10.5,10.5]
y_lines22=[0,16.5]

x_lines32=[10.5,21]
y_lines32=[16.5,16.5]

x_lines42=[21,21]
y_lines42=[0,16.5]


fig3 = plt.figure(figsize=(20,10))
fig3.suptitle('Suture 2D trajectory')

count=1
for i in range(12,20):
    pos_name=f"Rep{i+1}_{user_name}_SuturePos_x.txt"
    vel_name=f"Rep{i+1}_{user_name}_SutureVel_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    #?subplot_name.plot(data_pos['x1'], data_pos['y1'],   color="salmon", linewidth="2")

    plt.subplot(2,4,count)
    
    plt.plot(x_lines1, y_lines1, color="pink", lw=2)
    plt.plot(x_lines2, y_lines2, color="pink", lw=2)
    plt.plot(x_lines3, y_lines3, color="pink", lw=2)
    plt.plot(x_lines4, y_lines4, color="pink", lw=2)
    plt.plot(x_lines12, y_lines12, color="pink", lw=2)
    plt.plot(x_lines22, y_lines22, color="pink", lw=2)
    plt.plot(x_lines32, y_lines32, color="pink", lw=2)
    plt.plot(x_lines42, y_lines42, color="pink", lw=2)
    plt.plot(data_pos['x1'], data_pos['y1'],   color="salmon", linewidth="2",zorder=1)
    plt.scatter(x_spheres, y_spheres, s=100, color="red",zorder=2)
    plt.xlabel('x[cm]')
    plt.ylabel('y[cm]')
    plt.legend()
    plt.grid()
    count+=1
#plt.show()

fig.savefig(f'Images\{user_name}_Incision_2D_Trajectory.png')
fig2.savefig(f'Images\{user_name}_Rings_2D_Trajectory.png')
fig3.savefig(f'Images\{user_name}_Suture_2D_Trajectory.png')