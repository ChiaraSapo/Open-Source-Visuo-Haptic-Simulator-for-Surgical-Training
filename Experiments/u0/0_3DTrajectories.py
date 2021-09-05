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
    
    #plt.subplot(2,3,i)
    ax=fig.add_subplot(projection='3d')
    ax.plot(data_pos['x1'],data_pos['y1'],data_pos['z1'], label="Trajectory", color="palegreen", linewidth="2")
    ax.set_xlabel('x[cm]')
    ax.set_ylabel('y[cm]')
    ax.set_zlabel('z[cm]')
    ax.grid()
    ax.azim = -90
    ax.dist = 10
    ax.elev = 20
    fig.savefig(f'Images\{user_name}_Incision_3D_Trajectory_{i}.png'.format(ax.azim, ax.dist, ax.elev))


for i in range(3,5):
    pos_name=f"Rep{i}_{user_name}_Incision3Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision3Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    #plt.subplot(2,3,i)
    ax=fig.add_subplot(projection='3d')
    ax.plot(data_pos['x1'],data_pos['y1'],data_pos['z1'], label="Trajectory", color="palegreen", linewidth="2")
    ax.set_xlabel('x[cm]')
    ax.set_ylabel('y[cm]')
    ax.set_zlabel('z[cm]')
    ax.grid()
    ax.azim = -90
    ax.dist = 10
    ax.elev = 20
    fig.savefig(f'Images\{user_name}_Incision_3D_Trajectory_{i}.png'.format(ax.azim, ax.dist, ax.elev))



for i in range(5,7):
    pos_name=f"Rep{i}_{user_name}_Incision4Pos_Double_x.txt"
    vel_name=f"Rep{i}_{user_name}_Incision4Vel_Double_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])

    #plt.subplot(2,3,i)
    ax=fig.add_subplot(projection='3d')
    ax.plot(data_pos['x1'],data_pos['y1'],data_pos['z1'], label="Trajectory", color="palegreen", linewidth="2")
    ax.set_xlabel('x[cm]')
    ax.set_ylabel('y[cm]')
    ax.set_zlabel('z[cm]')
    ax.azim = -90
    ax.dist = 10
    ax.elev = 20
    ax.grid()


    fig.savefig(f'Images\{user_name}_Incision_3D_Trajectory_{i}.png'.format(ax.azim, ax.dist, ax.elev))
    


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
    
    ax=fig2.add_subplot(projection='3d')
    ax.plot(data_pos['x1'],data_pos['y1'],data_pos['z1'], label="Trajectory", color="palegreen", linewidth="2")
    ax.set_xlabel('x[cm]')
    ax.set_ylabel('y[cm]')
    ax.set_zlabel('z[cm]')
    ax.grid()
    ax.azim = -90
    ax.dist = 10
    ax.elev = 20

    fig2.savefig(f'Images\{user_name}_Rings_3D_Trajectory_{i}.png'.format(ax.azim, ax.dist, ax.elev))

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



count=1
for i in range(12,20):
    fig3 = plt.figure(figsize=(20,10))
    fig3.suptitle('Suture 2D trajectory')
    pos_name=f"Rep{i+1}_{user_name}_SuturePos_x.txt"
    vel_name=f"Rep{i+1}_{user_name}_SutureVel_v.txt"

    data_pos = pd.read_csv(pos_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    data_vel = pd.read_csv(vel_name,  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    #?subplot_name.plot(data_pos['x1'], data_pos['y1'],   color="palegreen", linewidth="2")

    
    ax=fig3.add_subplot(projection='3d')
    x=data_pos['x1']
    y=data_pos['y1']
    z=data_pos['z1']
    ax.plot(x,y,z, label="Trajectory", color="palegreen", linewidth="2")
    ax.set_xlabel('x[cm]')
    ax.set_ylabel('y[cm]')
    ax.set_zlabel('z[cm]')
    ax.azim = -90
    ax.dist = 10
    ax.elev = 20
    ax.grid()

    fig3.savefig(f'Images\{user_name}_Suture_3D_Trajectory_{i}.png'.format(ax.azim, ax.dist, ax.elev))
    count+=1

#plt.show()


