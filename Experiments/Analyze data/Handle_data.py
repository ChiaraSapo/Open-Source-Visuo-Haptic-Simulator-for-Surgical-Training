import tkinter as tk
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse
import numpy as np
from scipy.interpolate import interp2d
import os
import seaborn as sns
from scipy.stats import pointbiserialr
from scipy.spatial import distance
import math



# Path length functions

def Incision_Path_Length_per_user(incision_data):
    
    tot_dist_reps=[]
    for data_pos in incision_data:
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1))
        for i in range(1,len(x_list1)):
            dist.append( distance.euclidean( points[i],points[i-1] )  )
        tot_dist=sum(dist)
        tot_dist_reps.append(tot_dist)
    return tot_dist_reps


def Rings_Path_Length_per_user(rings_data):
    
    tot_dist_reps=[]
    for data_pos in rings_data:
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1))
        for i in range(1,len(x_list1)):
            dist.append( distance.euclidean( points[i],points[i-1] )  )
        tot_dist=sum(dist)
        tot_dist_reps.append(tot_dist)
    return tot_dist_reps


def Suture_Path_Length_per_user(suture_data):

    tot_dist_reps=[]
    for data_pos in suture_data:
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1))
        for i in range(len(x_list1)):
            dist.append( distance.euclidean( points[i],points[i-1] )  )
        tot_dist=sum(dist)
        tot_dist_reps.append(tot_dist)
    return tot_dist_reps


def Suture_Path_Length_per_user_wrt_peaks(suture_data):

    boxes_x=[8,8,13.5,13.5]
    boxes_y=[3,10,6,14]
    boxSize=2
    tot_dist_reps_1=np.zeros([len(suture_data), len(boxes_x)])
    k=0
    for data_pos in suture_data:
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()                
        points=list(zip(x_list1,y_list1))
        for i in range(1,len(x_list1)):
            for box in range(len(boxes_x)):
                if x_list1[i] >= (boxes_x[box]-boxSize) and x_list1[i]<=(boxes_x[box]+boxSize) and y_list1[i] >= (boxes_y[box]-boxSize) and y_list1[i]<=(boxes_y[box]+boxSize):
                    tot_dist_reps_1[k, box] += distance.euclidean( points[i],points[i-1] )  
        k+=1
    return tot_dist_reps_1


def Incision_Path_Length_per_user_from_7(incision_data):

    total_mean_reps=[]
    for data_pos in incision_data:
        x_list1 = data_pos['x1'].to_list()
        dist=[]
        for i in range(len(x_list1)):
            dist.append( abs(x_list1[i]-7) )
        dist=np.array(dist)
        mean=dist.mean()
        total_mean_reps.append(mean)
    return total_mean_reps


def Incision_Path_Length_per_user_from_1_5(incision_data):
    
    total_mean_reps=[]
    for data_pos in incision_data:
        y_list1 = data_pos['y1'].to_list()
        dist=[]
        for i in range(len(y_list1)):
            dist.append( abs(y_list1[i]-1.5) )
        dist=np.array(dist)
        mean=dist.mean()
        total_mean_reps.append(mean)
    return total_mean_reps












# Time in repetitions functions

def Incision_Time(incision_data):

    duration=[]
    count=1
    for data_pos in incision_data:
        print(count)
        temp=data_pos['Time']
        duration.append(temp[temp.size-1])
        count+=1
    print(len(duration))
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Incision repetitions time')
    x=np.array(range(7))
    plt.scatter([1,2,3,4,5,6], duration, s=400, color="darkturquoise")
    plt.xlabel('Repetitions')
    plt.ylabel('Time[dt]')
    plt.legend()
    plt.xticks(x)
    plt.grid()
    fig.savefig(f'Images\{user_name}_Incision_Time_Reps.png')


def Rings_Time(rings_data):
    
    duration=[]
    for data_pos in rings_data:
        temp=data_pos['Time']
        duration.append(temp[temp.size-1])
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Rings repetitions time')
    x=np.array(range(7))
    plt.scatter([1,2,3,4,5,6], duration, s=400, color="darkturquoise")
    plt.xlabel('Repetitions')
    plt.ylabel('Time[dt]')
    plt.legend()
    plt.xticks(x)
    plt.grid()
    fig.savefig(f'Images\{user_name}_Rings_Time_Reps.png')


def Suture_Time():
    
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Suture repetitions time')
    with open('Sut.txt') as f:
        lines = f.readlines()
        text = ''.join(lines).strip()
        groups = text.split('\n\n')
        result = []
        duration=[]
        for g in groups:
            array = np.array(g.strip().split('\n'))
            result.append([float(x) for x in array])    
    temp_0=result[0]
    temp_1=result[1]
    temp_2=result[2]
    temp_3=result[3]
    temp_4=result[4]
    temp_5=result[5]
    temp_6=result[6]
    temp_7=result[7]
    temp_8=result[8]
    duration=[]
    duration.append(temp_1[-1]-temp_0[0])
    duration.append(temp_2[-1]-temp_1[0])
    duration.append(temp_3[-1]-temp_2[0])
    duration.append(temp_4[-1]-temp_3[0])
    duration.append(temp_5[-1]-temp_4[0])
    duration.append(temp_6[-1]-temp_5[0])
    duration.append(temp_7[-1]-temp_6[0])
    duration.append(temp_8[-1]-temp_7[0])
    x=np.array(range(9))
    plt.scatter([1,2,3,4,5,6,7,8], duration, s=400, color="darkturquoise")
    plt.xlabel('Repetitions')
    plt.ylabel('Time[dt]')
    plt.legend()
    plt.xticks(x)
    plt.grid()
    fig.savefig(f'Images\{user_name}_Suture_Time_Reps.png')









# Height functions

def Incision_Height(incision_data, peaks=None, filename=''):
    
    fig = plt.figure(figsize=(20,10))
    fig.suptitle(f'{filename} Incision height', fontsize='x-large')
    i=1
    for data_pos in incision_data:
        ax=fig.add_subplot(2,3,i)
        plt.plot(data_pos['Time'], data_pos['z1'],  color="maroon", linewidth="2")
        triangle1 = Rectangle( (-2,0), data_pos['Time'].size, 1.2, fc='pink', ec=(0,0,0,0), lw=2)
        ax.add_artist(triangle1)
        plt.xlabel('Time[dt]', fontsize='x-large')
        plt.ylabel('Height[cm]', fontsize='x-large')
        plt.ylim([-9,8])
        plt.grid()
        if peaks:
            [plt.axvline(p, c='C3', linewidth=2, ls='--') for p in peaks[i-1]]
        i+=1
    plt.tight_layout()
    fig.savefig(f'Images\{filename}_Incision_Height.png')

def Rings_Height(rings_data, rings_peaks, filename=''):

    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle(f'{filename} Rings height', fontsize='x-large')
    count=1
    for data_pos in rings_data:
        height=[4] * data_pos['Time'].size
        ax=fig2.add_subplot(2,3,count) 
        plt.plot(data_pos['Time'], data_pos['z1'],  color="maroon", linewidth="2")
        plt.plot(data_pos['Time'], height, color=(0.5,0.3,1,1), linewidth="2") # center of the rings
        
        rec1=Rectangle( (0,0), data_pos['Time'].size-1, 1.8+0.4, fc="pink", ec=(0,0,0,0), lw=2)
        rec2=Rectangle( (0,1.8+0.4), data_pos['Time'].size-1, 1.2+0.4, fc="lightgreen", ec=(0,0,0,0), lw=2)
        rec3 = Rectangle((0,3+0.4), data_pos['Time'].size-1, 2+0.4, fc="lavender", ec=(0,0,0,0), lw=2)
        rec4=Rectangle( (0,5+0.4), data_pos['Time'].size-1, 1.2+0.4, fc="lightgreen", ec=(0,0,0,0), lw=2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(rec3)
        ax.add_artist(rec4)
        temp=data_pos['Time'].values
        plt.xlabel('Time[dt]', fontsize='x-large')
        plt.ylabel('Height[cm]', fontsize='x-large')
        plt.xlim([temp[0],temp[-1]])
        plt.ylim([0.5,15])
        plt.grid()
        if rings_peaks!=[]:
            [plt.axvline(p, c='C3', linewidth=2, ls='--') for p in rings_peaks[count-1]]
        count+=1
    plt.tight_layout()
    fig2.savefig(f'Images\{filename}_Rings_Height.png')

def Suture_Height(suture_data , suture_peaks=[], filename=''):
    
    fig3 = plt.figure(figsize=(20,10))
    fig3.suptitle(f'{filename}Suture height', fontsize='x-large')
    count=1
    for data_pos in suture_data:
        height=[1.5] * data_pos['Time'].size
        ax=fig3.add_subplot(2,4,count)
        plt.plot(data_pos['Time'], data_pos['z1'],  color="maroon", linewidth="2",zorder=2)
        temp=np.array(data_pos['Time'])
        tr=Rectangle((0,0),len(temp), 2.5,color="pink",zorder=1)
        ax.add_artist(tr)
        plt.xlabel('Time[dt]', fontsize='x-large')
        plt.ylabel('Height[cm]', fontsize='x-large')
        plt.xlim([0.5,temp[-1]])
        plt.ylim([-2,13])
        plt.grid()
        if suture_peaks:
            [plt.axvline(p, c='C3', linewidth=2, ls='--') for p in suture_peaks[count-1]]
        count+=1
    plt.tight_layout()
    fig3.savefig(f'Images\{filename}_Suture_Height.png')








# Trajectory functions

def Incision_Trajectory(incision_data, filename=''):
    
    fig = plt.figure(figsize=(20,10))
    fig.suptitle(f'{filename} Incision 2D trajectory', fontsize='x-large')
    x_lines4=[7.2,7.2]
    y_lines4=[11,22]
    i=1
    for data_pos in incision_data:
        ax=fig.add_subplot(2,3,i)
        plt.plot(data_pos['x1'], data_pos['y1'],   color="maroon", linewidth="2",zorder=4)
        plt.xlabel('x[cm]', fontsize='x-large')
        plt.ylabel('y[cm]', fontsize='x-large')
        triangle1 = Rectangle( (6.2,11), 1.8, 11, fc=(0.5,0.3,1,0.5), ec=(0,0,0,0), lw=2,zorder=2)
        triangle2=Rectangle((0,11),14,11,color="pink",zorder=1) 
        plt.plot(x_lines4, y_lines4, color="pink", lw=2,zorder=3)
        ax.add_artist(triangle1)
        ax.add_artist(triangle2)
        plt.xlim([-1,15])
        plt.ylim([10,23])
        plt.grid()
        i+=1
    plt.tight_layout()
    fig.savefig(f'Images\{filename}_Incision_2D_Trajectory.png')


def Rings_Trajectory(rings_data, filename=''):

    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle(f'{filename} Rings 2D trajectory', fontsize='x-large')
    x_rings=[7,7,13,13]
    y_rings=[5,13,8.5,15.5]
    count=1
    for data_pos in rings_data:
        ax=fig2.add_subplot(2,3,count) 
        triangle2=Rectangle((0,0),10,20,color="pink",zorder=1) 
        triangle3=Rectangle((11,0),10,20,color="pink",zorder=1)
        ax.add_artist(triangle2)
        ax.add_artist(triangle3) 
        plt.plot(data_pos['x1'], data_pos['y1'],   color="maroon", linewidth="2",zorder=2)
        for i in range(4):
            ell1=Ellipse((x_rings[i], y_rings[i]), width=3, height=1.5, color="forestgreen",zorder=3)
            ax.add_patch(ell1)
        plt.xlabel('x[cm]', fontsize='x-large')
        plt.ylabel('y[cm]', fontsize='x-large')
        plt.xlim([-1,22])
        plt.ylim([-1,21])
        plt.grid()
        count+=1
    plt.tight_layout()
    fig2.savefig(f'Images\{filename}_Rings_2D_Trajectory.png')



def Suture_Trajectory(suture_data, filename=''):

    x_spheres=[8,8,13.5,13.5]
    y_spheres=[4,10,4.5,10.5]
    fig3 = plt.figure(figsize=(20,10))
    fig3.suptitle(f'{filename} Suture 2D trajectory', fontsize='x-large')
    count=1
    for data_pos in suture_data:
        ax=fig3.add_subplot(2,4,count)
        triangle2=Rectangle((0,0),10,16.5,color="pink",zorder=1) 
        triangle3=Rectangle((10.5,0),10,16.5,color="pink",zorder=1) 
        plt.plot(data_pos['x1'], data_pos['y1'],   color="maroon", linewidth="2",zorder=2)
        plt.scatter(x_spheres, y_spheres, s=100, color="red",zorder=3)
        ax.add_artist(triangle2)
        ax.add_artist(triangle3)
        plt.xlim([-1,22])
        plt.ylim([-1,17.5])
        plt.xlabel('x[cm]', fontsize='x-large')
        plt.ylabel('y[cm]', fontsize='x-large')
        plt.grid()
        count+=1
    plt.tight_layout()
    fig3.savefig(f'Images\{filename}_Suture_2D_Trajectory.png')






# Metrics plots per user

def Incision_Path_Length_plot_per_user(incision_dist_reps, NSurgeons, NControl):
    Ntot=NSurgeons+NControl
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Surgeons Trajectory Length in incision')
    j=1
    plot_width_sur=math.ceil(NSurgeons/2)
    plot_width_cont=math.ceil(NControl/2)  
    for i in range(NSurgeons):
        fig.add_subplot(2,plot_width_sur,j)
        plt.title(f's{i}')
        plt.plot([1,2,3,4,5,6], np.array(incision_dist_reps[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Trajectory Length')
        plt.xlabel('Incision repetition')
        plt.grid()
        j+=1  
    fig.savefig(f'Images\Surgeons_incision_trajectories.png')
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle('Control Trajectory Length in incision')
    j=1
    for i in range(NSurgeons,Ntot):
        fig2.add_subplot(2,plot_width_cont,j)
        plt.title(f'u{i}')
        plt.plot([1,2,3,4,5,6], np.array(incision_dist_reps[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Trajectory Length')
        plt.xlabel('Incision repetition')
        plt.grid()
        j+=1
    fig2.savefig(f'Images\Control_incision_trajectories.png')




def Rings_Path_Length_plot_per_user(rings_dist_reps, NSurgeons, NControl):
    
    Ntot=NSurgeons+NControl
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Surgeons Trajectory Length in rings')
    j=1
    plot_width_sur=math.ceil(NSurgeons/2)
    plot_width_cont=math.ceil(NControl/2) 
    for i in range(NSurgeons):
        fig.add_subplot(2,plot_width_sur,j)
        plt.title(f's{i}')
        plt.plot([1,2,3,4,5,6], np.array(rings_dist_reps[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Trajectory Length')
        plt.xlabel('Rings repetition')
        plt.grid()
        j+=1  
    fig.savefig(f'Images\Surgeons_rings_trajectories.png')
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle('Control Trajectory Length in rings')
    j=1
    for i in range(NSurgeons,Ntot):
        fig2.add_subplot(2,plot_width_cont,j)
        plt.title(f'u{i}')
        plt.plot([1,2,3,4,5,6], np.array(rings_dist_reps[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Trajectory Length')
        plt.xlabel('Rings repetition')
        plt.grid()
        j+=1
    fig2.savefig(f'Images\Control_rings_trajectories.png')




def Suture_Path_Length_plot_per_user(suture_dist_reps, NSurgeons, NControl):
    Ntot=NSurgeons+NControl
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Surgeons Trajectory Length  in suture')
    j=1
    plot_width_sur=math.ceil(NSurgeons/2)
    plot_width_cont=math.ceil(NControl/2)
    for i in range(NSurgeons):
        fig.add_subplot(2,plot_width_sur,j)
        x=range(1,len(suture_dist_reps[i])+1)
        plt.title(f's{i}')
        plt.plot(x, suture_dist_reps[i], color="darkorchid", lw=2.5)
        plt.ylabel('Trajectory Length')
        plt.xlabel('Suture repetition')
        plt.grid()
        j+=1  
    fig.savefig(f'Images\Surgeons_suture_trajectories.png')
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle('Control Trajectory Length in suture')
    j=1
    for i in range(NSurgeons,Ntot):
        fig2.add_subplot(2,plot_width_cont,j)
        plt.title(f'u{i}')
        x=range(1,len(suture_dist_reps[i])+1)
        plt.plot(x, np.array(suture_dist_reps[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Trajectory Length')
        plt.xlabel('Suture repetition')
        plt.grid()
        j+=1
    fig2.savefig(f'Images\Control_suture_trajectories.png')




def Incision_Path_Length_plot_per_user_from_7(incision_dist_7, NSurgeons, NControl):
    Ntot=NSurgeons+NControl
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Surgeons Mean distance from x=7')
    j=1
    plot_width_sur=math.ceil(NSurgeons/2)
    plot_width_cont=math.ceil(NControl/2)
    for i in range(NSurgeons):
        fig.add_subplot(2,plot_width_sur,j)
        plt.title(f's{i}')
        plt.plot([1,2,3,4,5,6], np.array(incision_dist_7[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Mean distance')
        plt.xlabel('Incision repetition')
        plt.grid()
        j+=1  
    fig.savefig(f'Images\Surgeons_incision_7.png')
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle('Control Mean distance from x=7')
    j=1
    for i in range(NSurgeons,Ntot):
        fig2.add_subplot(2,plot_width_cont,j)
        plt.title(f'u{i}')
        plt.plot([1,2,3,4,5,6], np.array(incision_dist_7[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Mean distance')
        plt.xlabel('Incision repetition')
        plt.grid()
        j+=1
    fig2.savefig(f'Images\Control_incision_7.png')



def Incision_Path_Length_plot_per_user_from_1_5(incision_dist_1_5, NSurgeons, NControl):
    Ntot=NSurgeons+NControl
    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Surgeons Mean distance from z=1.5')
    j=1
    plot_width_sur=math.ceil(NSurgeons/2)
    plot_width_cont=math.ceil(NControl/2)   
    for i in range(NSurgeons):
        fig.add_subplot(2,plot_width_sur,j)
        plt.title(f's{i}')
        plt.plot([1,2,3,4,5,6], np.array(incision_dist_1_5[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Mean distance')
        plt.xlabel('Incision repetition')
        plt.grid()
        j+=1  
    fig.savefig(f'Images\Surgeons_incision_1_5.png')
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle('Control Mean distance from z=1.5')
    j=1
    for i in range(NSurgeons,Ntot):
        fig2.add_subplot(2,plot_width_cont,j)
        plt.title(f'u{i}')
        plt.plot([1,2,3,4,5,6], np.array(incision_dist_1_5[i]), color="darkorchid", lw=2.5)
        plt.ylabel('Mean distance')
        plt.xlabel('Incision repetition')
        plt.grid()
        j+=1
    fig2.savefig(f'Images\Control_incision_1_5.png')





# Metrics for all users

def Data_Rings_Peaks(total_peaks):

    # Create Pandas dataframe for the rings peaks
    names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
    peaks_dataframe = pd.DataFrame(columns=['Subject', 'Surgeon', 'Age',  'Repetition', 'Peak score'])
    index = 0
    for i, (subject, is_surgeon, age) in enumerate(zip(names, surgeons, ages)):
        for rep in range(6):
            peaks_dataframe.loc[index] = [subject, is_surgeon, age, rep, len(total_peaks[index])]
            index += 1
    # Save data to excel file
    file_name = f'Data\Peaks.xlsx'
    peaks_dataframe.to_excel(file_name)


def Data_Suture_Box(traj_in_boxes):

    names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
    sut_box_dataframe = pd.DataFrame(columns=['Subject', 'Surgeon', 'Age',  'Repetition', 'Box1', 'Box2', 'Box3', 'Box4'])
    index = 0
    person=0
    for i, (subject, is_surgeon, age) in enumerate(zip(names, surgeons, ages)):
        for rep in range(8):
            sut_box_dataframe.loc[index] = [subject, is_surgeon, age, rep, traj_in_boxes[person][rep][0], traj_in_boxes[person][rep][1], traj_in_boxes[person][rep][2], traj_in_boxes[person][rep][3]]
            index += 1
        person += 1
    # Save data to excel file
    file_name = f'Data\Sut_box.xlsx'
    sut_box_dataframe.to_excel(file_name)


def Data_total(incision_dist_reps, suture_dist_reps, rings_dist_reps, incision_dist_7, incision_dist_1_5):
    
    # Create Pandas dataframe for the metrics
    results_dict = {'incision_dist_reps': incision_dist_reps,
                    'suture_dist_reps': suture_dist_reps,
                    'rings_dist_reps': rings_dist_reps,
                    'incision_dist_7': incision_dist_7,
                    'incision_dist_1_5': incision_dist_1_5}
    testList = ['incision_dist_reps','suture_dist_reps', 'rings_dist_reps', 'incision_dist_7', 'incision_dist_1_5']
    for testName in testList:
        if testName=='suture_dist_reps':
            names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
            surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
            ages = [67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
        else: 
            names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
            surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
            ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
        df2 = pd.DataFrame(columns=['Subject', 'Surgeon', 'Age', 'Test', 'Repetition', 'Score'])
        index = 0
        for i, (subject, is_surgeon, age) in enumerate(zip(names, surgeons, ages)):
            for test in results_dict.keys():
                if test == testName:
                    for rep, result in enumerate(results_dict[test][i]):
                        df2.loc[index] = [subject, is_surgeon, age, test, float(rep+1), result]
                        index += 1
        df2['Test'] = df2['Test'].factorize()[0]
        with sns.axes_style("white"):
            corr_matrix = df2.drop('Subject', axis=1).corr(method ='pearson')
            corr_matrix.drop(['Test', 'Score'], axis=0, inplace=True)
            fig = plt.figure(figsize=(5, 8))
            plt.title(f'Cross correlation among features and {testName}')
            ax = sns.heatmap(
                corr_matrix[['Score']],
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                #square=True,
                linewidths=.5,
                annot_kws={"size": 10},
                cbar_kws={"shrink": .8},
                vmin=-1,
                vmax=1
            )
            plt.yticks(rotation=0)
            plt.tight_layout()
            fig.savefig(f'Images\cross_corr_matrix_{testName}.png')
        # Save data to excel file
        file_name = f'Data\{testName}.xlsx'
        df2.to_excel(file_name)










# UNUSED FUNCTIONS


def Incision_colormap(incision_data):

    j=1
    for data_pos_1 in incision_data:
        fig = plt.figure(figsize=(7,10))
        fig.suptitle('Incision colormap')

        x_list1 = data_pos_1['x1'].to_list()
        y_list1 = data_pos_1['y1'].to_list()
        z_list1 = data_pos_1['z1'].to_list()

        x_list=[]
        y_list=[]
        z_list=[]
        
        for i in range(len(x_list1)):
            if 5.5 < x_list1[i] < 8.5 and 9 < y_list1[i] < 23:
                x_list.append(x_list1[i])
                y_list.append(y_list1[i])
                z_list.append(z_list1[i])

        #ax=fig.add_subplot(2,3,j)
        plt.scatter(x_list, y_list, c=z_list, label='height')
        plt.colorbar()
        plt.legend()
        plt.xlabel('x coordinate')
        plt.ylabel('y coordinate')
        #plt.show()


        f = interp2d(x_list, y_list, z_list, kind="linear")
        x_coords = np.arange(min(x_list), max(x_list) + 0.2, 0.2)
        y_coords = np.arange(min(y_list), max(y_list) + 1)
        Z = f(x_coords, y_coords)


        #plt.imshow(Z,extent=[5.5,8.5,9,23])

        plt.scatter(x_list, y_list, 400, facecolors='none')
        

        fig.savefig(f'Images\{user_name}_Incision_Rep{j}_Colormap.png')
        j+=1


def Suture_colormap(suture_data):

    j=13

    for data_pos_1 in suture_data:
    
        fig = plt.figure(figsize=(7,10))
        fig.suptitle('Suture repetitions time')

        x_list1 = data_pos_1['x1'].to_list()
        y_list1 = data_pos_1['y1'].to_list()
        z_list1 = data_pos_1['z1'].to_list()

        x_list=[]
        y_list=[]
        z_list=[]
        

        for i in range(len(x_list1)):
            if 0 < x_list1[i] < 20 and 0 < y_list1[i] < 17:
                x_list.append(x_list1[i])
                y_list.append(y_list1[i])
                z_list.append(z_list1[i])

        #ax=fig.add_subplot(2,3,j)
        plt.scatter(x_list, y_list, c=z_list, label='height')
        plt.colorbar()
        plt.legend()
        plt.xlabel('x coordinate')
        plt.ylabel('y coordinate')


        f = interp2d(x_list, y_list, z_list, kind="linear")
        x_coords = np.arange(min(x_list), max(x_list) + 0.2, 0.2)
        y_coords = np.arange(min(y_list), max(y_list) + 1)
        Z = f(x_coords, y_coords)


        #plt.imshow(Z,extent=[min(x_list),max(x_list),0,18])

        plt.scatter(x_list, y_list, 400, facecolors='none')
        

        fig.savefig(f'Images\{user_name}_Suture_Rep{j}_Colormap.png')
        j+=1





