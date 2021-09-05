import tkinter as tk
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle


ConfigName=open('Name.txt')
for line in ConfigName:
    pass
user_name = line
ConfigName.close()
print(user_name)


fig = plt.figure(figsize=(20,10))
fig.suptitle('Incision height with respect to skin length')

for i in range(1,3):
    pos_name=f"Rep{i}_{user_name}_Incision2Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision2Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    
    ax=fig.add_subplot(2,3,i)
    plt.plot(data_pos['y1'], data_pos['z1'],  color="palegreen", linewidth="2")
    triangle1 = Rectangle( (-2,0), data_pos['Time'].size, 1.5, fc=(1,0,0,0.5), ec=(0,0,0,0), lw=2)
    ax.add_artist(triangle1)
    plt.xlabel('y[cm]')
    plt.ylabel('Height[cm]')
    plt.ylim([-3,7])
    plt.xlim([9,25])
    plt.legend()
    plt.grid()

for i in range(3,5):
    pos_name=f"Rep{i}_{user_name}_Incision3Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision3Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    ax=fig.add_subplot(2,3,i)
    plt.plot(data_pos['y1'], data_pos['z1'],  color="palegreen", linewidth="2")
    triangle1 = Rectangle( (-2,0), data_pos['Time'].size, 1.5, fc=(1,0,0,0.5), ec=(0,0,0,0), lw=2)
    ax.add_artist(triangle1)
    plt.xlabel('y[cm]')
    plt.ylabel('Height[cm]')
    plt.ylim([-3,7])
    plt.xlim([9,25])
    plt.legend()
    plt.grid()


for i in range(5,7):
    pos_name=f"Rep{i}_{user_name}_Incision4Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision4Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    ax=fig.add_subplot(2,3,i)
    plt.plot(data_pos['y1'], data_pos['z1'],  color="palegreen", linewidth="2")
    triangle1 = Rectangle( (-2,0), data_pos['Time'].size, 1.5, fc=(1,0,0,0.5), ec=(0,0,0,0), lw=2)
    ax.add_artist(triangle1)
    
    plt.xlabel('y[cm]')
    plt.ylabel('Height[cm]')
    plt.ylim([-3,7])
    plt.xlim([9,25])
    plt.legend()
    plt.grid()
#plt.show()



x_spheres=[4,10,4.5,10.5]
y_spheres=[2,2,2,2]
fig3 = plt.figure(figsize=(20,10))
fig3.suptitle('Suture height length')

count=1
for i in range(12,20):
    pos_name=f"Rep{i+1}_{user_name}_SuturePos_x.txt"
    vel_name=f"Rep{i+1}_{user_name}_SutureVel_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    height=[1.5] * data_pos['y1'].size
    plt.subplot(2,4,count)
    plt.plot(data_pos['y1'], data_pos['z1'],  color="palegreen", linewidth="2",zorder=1)
    plt.plot(data_pos['y1'], height, color="pink", linewidth="3")
    plt.scatter(x_spheres, y_spheres, s=200, color="red",zorder=2)
    plt.ylim([-2,15])
    plt.xlabel('y[s]')
    plt.ylabel('Height[cm]')
    plt.legend()
    plt.grid()
    count+=1
#plt.show()

fig.savefig(f'Images\{user_name}_Incision_Height_Length.png')
fig3.savefig(f'Images\{user_name}_Suture_Height_Length.png')