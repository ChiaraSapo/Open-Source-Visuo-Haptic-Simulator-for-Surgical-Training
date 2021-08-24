import tkinter as tk
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def Window3(win3):

    # Read user name
    Config=open('Config.txt')
    for line in Config:
        pass
    user_name = line
    Config.close()

    # Read user data (last lines of the file)
    fileName=f"{user_name}.txt"
    User=open(fileName)
    lines1=User.readlines()
    lines=lines1[-4:]
    date=lines[0]
    time=lines[1]
    task_type=lines[2]
    station_type=lines[3]
    #points=lines[4]
    points=2
    User.close()

    print(task_type)

    # Read plot data
    if task_type=="Suture\n":
        data_pos = pd.read_csv("SutureTask_pos_x.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
        data_vel = pd.read_csv("SutureTask_vel_v.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
        data_force = pd.read_csv("SutureTask_force_f.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    elif task_type=="Rings\n":
        data_pos = pd.read_csv("RingsTask_pos_x.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
        data_vel = pd.read_csv("RingsTask_vel_v.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
        data_force = pd.read_csv("RingsTask_force_f.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
    elif task_type=="Incision\n":
        data_pos = pd.read_csv("IncisionTask_pos_x.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y 1', 'z1'])
        data_vel = pd.read_csv("IncisionTask_vel_v.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])
        data_force = pd.read_csv("IncisionTask_force_f.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, names=['Time', 'x1', 'y1', 'z1'])


    # Plot figure 1
    fig=plt.figure(figsize=(10,8))
    ax=fig.add_subplot(projection='3d')
    ax.plot(data_pos['x1'],data_pos['y1'],data_pos['z1'], label="Trajectory", color="salmon", linewidth="3.5")
    ax.set_title("End effector position in space")
    ax.set_xlabel('x direction')
    ax.set_ylabel('y direction')
    ax.set_zlabel('z direction')
    ax.grid()

    bar1 = FigureCanvasTkAgg(fig, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    # Plot figure 2
    fig, ((ax, ax1), (ax2, ax3)) = plt.subplots(2,2)
    fig.suptitle('Position, Velocity,  Force')

    ax.plot(data_pos['x1'], data_pos['y1'], label="pos_x", color="salmon", linewidth="3.5")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid()

    ax1.plot(data_pos['Time'],data_pos['x1'], label="pos_x", color="salmon", linewidth="3.5")
    ax1.plot(data_pos['Time'],data_pos['y1'], label="pos_y", color="darkturquoise", linewidth="3.5")
    ax1.plot(data_pos['Time'],data_pos['z1'], label="pos_z", color="palegreen", linewidth="3.5")
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Positions')
    ax1.legend()
    ax1.grid()

    ax2.plot(data_vel['Time'],data_vel['x1'], label="vel_x", color="salmon", linewidth="3.5")
    ax2.plot(data_vel['Time'],data_vel['y1'], label="vel_y", color="darkturquoise", linewidth="3.5")
    ax2.plot(data_vel['Time'],data_vel['z1'], label="vel_z", color="palegreen", linewidth="3.5")
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Velocities')
    ax2.legend()
    ax2.grid()

    ax3.plot(data_force['Time'],data_force['x1'], label="force_x", color="salmon", linewidth="3.5")
    ax3.plot(data_force['Time'],data_force['y1'], label="force_y", color="darkturquoise", linewidth="3.5")
    ax3.plot(data_force['Time'],data_force['z1'], label="force_z", color="palegreen", linewidth="3.5")
    ax3.set_xlabel('Time [s]')
    ax3.set_ylabel('Forces')
    ax3.legend()
    ax3.grid()

    bar2 = FigureCanvasTkAgg(fig, root)
    bar2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    # Text 
    text=f"Hi {user_name}, you made {points} points!"
    label1 = tk.Label(root, text=text)
    label1.config(font=('Arial', 20))
    label1.place(x=50, y=50)

    text=f"Task simulation:{task_type} Date:{date} Time:{time} Station type:{station_type}"
    label1 = tk.Label(root, text=text)
    label1.config(font=('Arial', 15))
    label1.place(x=50, y=150)



if __name__ == "__main__":

    root = tk.Tk()
    Window3(root)
    root.mainloop()
