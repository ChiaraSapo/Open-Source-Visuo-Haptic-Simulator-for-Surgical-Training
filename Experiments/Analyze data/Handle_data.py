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
from matplotlib.pyplot import cm
import matplotlib.ticker as mtick
from scipy.signal import find_peaks


#################################################################################################
#################################################################################################
#################################################################################################


# 3D Path Length for Incision

def Incision_Path_Length_per_user(incision_data):
    #print("Incision PL reps: ", len(incision_data))
    tot_dist_reps=[]
    for data_pos in incision_data: # For each repetition
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        z_list1 = data_pos['z1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1,z_list1))
        for i in range(1,len(x_list1)):
            dist.append( distance.euclidean( points[i],points[i-1] )) #math.sqrt( (x_list1[i]-x_list1[i-1])**2 + (y_list1[i]-y_list1[i-1])**2 + (z_list1[i]-z_list1[i-1])**2) ) 
        tot_dist=sum(dist)
        tot_dist_reps.append(tot_dist)
    return tot_dist_reps


# 3D Path Length for Rings

def Rings_Path_Length_per_user_3D(rings_data):
    
    tot_dist_reps=[]
    for data_pos in rings_data:
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        z_list1 = data_pos['z1'].to_list()
        #print(z_list1)
        dist=[]
        points=list(zip(x_list1,y_list1,z_list1))
        for i in range(1,len(x_list1)):
            dist.append( distance.euclidean( points[i],points[i-1] )  )
        tot_dist=sum(dist)
        tot_dist_reps.append(tot_dist)
    return tot_dist_reps


# 2D Path Length for Rings

def Rings_Path_Length_per_user_2D(rings_data):
    
    tot_dist_reps=[]
    for data_pos in rings_data:
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        #print(z_list1)
        dist=[]
        points=list(zip(x_list1,y_list1))
        for i in range(1,len(x_list1)):
            dist.append( distance.euclidean( points[i],points[i-1] )  )
        tot_dist=sum(dist)
        tot_dist_reps.append(tot_dist)
    return tot_dist_reps


# 3D Path Length for Suture

def Suture_Path_Length_per_user(suture_data):

    tot_dist_reps=[]
    for data_pos in suture_data:
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        z_list1 = data_pos['z1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1,z_list1))
        for i in range(len(x_list1)):
            dist.append( distance.euclidean( points[i],points[i-1] )  )
        tot_dist=sum(dist)
        tot_dist_reps.append(tot_dist)
    return tot_dist_reps

#################################################################################################
#################################################################################################
#################################################################################################

# Mean distance from x=7 for Incision



# Maximum deviation from z=1.5 for Incision

def Incision_Min_Dist_1_5(incision_data):

    total_mean_reps=[]
    for data_pos in incision_data:
        z_list1 = np.array(data_pos['z1'].values)
        z_list1=z_list1[np.where(z_list1<=1.8)]
        dist=max(abs(z_list1-1.8))
        total_mean_reps.append(dist)
    return total_mean_reps


# Maximum deviation from x=7 for Incision

def Incision_Min_Dist_7(incision_data):

    total_mean_reps=[]
    for data_pos in incision_data:
        x_list1 = np.array(data_pos['x1'].values)
        dist=max(abs(x_list1-7))
        total_mean_reps.append(dist)
    return total_mean_reps



#################################################################################################
#################################################################################################
#################################################################################################





# Height for Incision

def Incision_Height(incision_data, peaks=None, filename=''):
    tot_dist_reps=[]
    i=1
    fig = plt.figure(figsize=(20,10))
    fig.suptitle(f'{filename} Incision z coordinate with respect to path length', fontsize=22)
    
    for data_pos in incision_data:        
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        z_list1 = data_pos['z1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1,z_list1))
        for j in range(1,len(x_list1)):
            dist.append(distance.euclidean( points[j],points[j-1] ))
        dist2=[]
        dist2.append(0)
        for k in range(len(dist)-1):
            dist2.append(dist2[k]+dist[k+1])
        dist2.append(dist2[-1]+dist[-1])
        dist_np=np.divide(np.array(dist2),dist2[-1])
        ax=fig.add_subplot(2,3,i)
        plt.plot(dist_np, data_pos['z1'].values[:],  color="maroon", linewidth="2")
        triangle1 = Rectangle( (0,0), len(dist_np), 1.2, fc='pink', ec=(0,0,0,0), lw=2)
        ax.add_artist(triangle1)
        plt.xlabel('Path length percentage', fontsize=20)
        plt.ylabel('z [cm]', fontsize=20)
        plt.ylim([-9,8])
        plt.rc('axes', titlesize=18)     # fontsize of the axes title
        plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=16)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=16)    # fontsize of the tick labels
        plt.rc('legend', fontsize=18)    # legend fontsize
        #plt.xlim([11,23])
        #plt.grid()
                
        vals = ax.get_xticks()
        ax.set_xticklabels(['{:,.0f}'.format(x*100) + '%' for x in vals])
        # if peaks:
        #     [plt.axvline(p, c='C3', linewidth=2, ls='--') for p in peaks[i-1]]
        i+=1
    plt.tight_layout()
    fig.savefig(f'Images\Incision\{filename}Incision_Height.png')


def Rings_Height(rings_data, peaks=None, filename=''):
    tot_dist_reps=[]
    i=1
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle(f'{filename} Rings z coordinate with respect to path length', fontsize=22)
    
    for data_pos in rings_data:        
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        z_list1 = data_pos['z1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1,z_list1))
        for j in range(1,len(x_list1)):
            dist.append(distance.euclidean( points[j],points[j-1] ))
        dist2=[]
        dist2.append(0)
        for k in range(len(dist)-1):
            dist2.append(dist2[k]+dist[k+1])
        dist2.append(dist2[-1]+dist[-1])
        dist_np=np.divide(np.array(dist2),dist2[-1])
        height=[4.4] * data_pos['y1'].size
        ax=fig2.add_subplot(2,3,i) 
        data_pos['z1'].rolling(25).mean() 
        plt.plot(dist_np, data_pos['z1'].values[:],  color="maroon", linewidth="2")
        plt.plot(dist_np, height, color=(0.5,0.3,1,1), linewidth="2") # center of the rings
        
        rec1=Rectangle( (0,0), len(dist_np), 1.8+0.4, fc="pink", ec=(0,0,0,0), lw=2)
        rec2=Rectangle( (0,1.8+0.4), len(dist_np), 1.2+0.4, fc="lightgreen", ec=(0,0,0,0), lw=2)
        rec3 = Rectangle((0,3+0.4), len(dist_np), 2+0.4, fc="lavender", ec=(0,0,0,0), lw=2)
        rec4=Rectangle( (0,5+0.4), len(dist_np), 1.2+0.4, fc="lightgreen", ec=(0,0,0,0), lw=2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(rec3)
        ax.add_artist(rec4)
        plt.xlabel('Path length percentage', fontsize=20)
        plt.ylabel('z [cm]', fontsize=20)
        
        plt.ylim([0,9])
        plt.rc('axes', titlesize=18)     # fontsize of the axes title
        plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=16)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=16)    # fontsize of the tick labels
        plt.rc('legend', fontsize=18)    # legend fontsize
        #plt.xlim([11,23])
        #plt.grid()
                
        vals = ax.get_xticks()
        ax.set_xticklabels(['{:,.0f}'.format(x*100) + '%' for x in vals])
        # if peaks:
        #     [plt.axvline(p, c='C3', linewidth=2, ls='--') for p in peaks[i-1]]
        i+=1
    plt.tight_layout()
    fig2.savefig(f'Images\Rings\{filename}Rings_Height.png')

# Height for Rings

def Rings_Height_wrt_y(rings_data, rings_peaks, filename=''):

    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle(f'{filename} Rings height', fontsize=20)
    count=1
    for data_pos in rings_data:
        height=[4.4] * data_pos['y1'].size
        ax=fig2.add_subplot(2,3,count) 
        data_pos['z1'].rolling(25).mean() 
        plt.plot(data_pos['y1'], data_pos['z1'],  color="maroon", linewidth="2")
        plt.plot(data_pos['y1'], height, color=(0.5,0.3,1,1), linewidth="2") # center of the rings
        
        rec1=Rectangle( (0,0), data_pos['y1'].size-1, 1.8+0.4, fc="pink", ec=(0,0,0,0), lw=2)
        rec2=Rectangle( (0,1.8+0.4), data_pos['y1'].size-1, 1.2+0.4, fc="lightgreen", ec=(0,0,0,0), lw=2)
        rec3 = Rectangle((0,3+0.4), data_pos['y1'].size-1, 2+0.4, fc="lavender", ec=(0,0,0,0), lw=2)
        rec4=Rectangle( (0,5+0.4), data_pos['y1'].size-1, 1.2+0.4, fc="lightgreen", ec=(0,0,0,0), lw=2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(rec3)
        ax.add_artist(rec4)
        temp=data_pos['y1'].values
        plt.xlabel('y [cm]', fontsize=22)
        plt.ylabel('z [cm]', fontsize=22)
        plt.rc('font', size=22)          # controls default text sizes
        plt.rc('axes', titlesize=22)     # fontsize of the axes title
        plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
        plt.rc('legend', fontsize=20)    # legend fontsize
        plt.xlim([5.3,17.5])
        plt.ylim([0.5,15])
        #plt.grid()
        
        # if rings_peaks!=[]:
        #     [plt.axvline(p, c='C3', linewidth=2, ls='--') for p in (rings_peaks[count-1])]
        count+=1
    plt.tight_layout()
    fig2.savefig(f'Images\Rings\{filename}_Rings_Height.png')



def Suture_Height(suture_data, peaks=None, filename=''):
    tot_dist_reps=[]
    i=1
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle(f'{filename} Suture z coordinate with respect to path length', fontsize=22)
    
    for data_pos in suture_data:        
        x_list1 = data_pos['x1'].to_list()
        y_list1 = data_pos['y1'].to_list()
        z_list1 = data_pos['z1'].to_list()
        dist=[]
        points=list(zip(x_list1,y_list1,z_list1))
        for j in range(1,len(x_list1)):
            dist.append(distance.euclidean( points[j],points[j-1] ))
        dist2=[]
        dist2.append(0)
        for k in range(len(dist)-1):
            dist2.append(dist2[k]+dist[k+1])
        dist2.append(dist2[-1]+dist[-1])
        dist_np=np.divide(np.array(dist2),dist2[-1])
        height=[4.4] * data_pos['y1'].size
        ax=fig2.add_subplot(2,4,i) 
        data_pos['z1'].rolling(25).mean() 
        plt.plot(dist_np, data_pos['z1'].values[:],  color="maroon", linewidth="2")
        tr=Rectangle((0,0),len(dist_np), 2.5,color="pink",zorder=1)
        ax.add_artist(tr)
        plt.xlabel('Path length percentage', fontsize=20)
        plt.ylabel('z [cm]', fontsize=20)
        
        plt.ylim([-2,13])
        plt.rc('axes', titlesize=18)     # fontsize of the axes title
        plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=16)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=16)    # fontsize of the tick labels
        plt.rc('legend', fontsize=18)    # legend fontsize
        #plt.xlim([11,23])
        #plt.grid()
                
        vals = ax.get_xticks()
        ax.set_xticklabels(['{:,.0f}'.format(x*100) + '%' for x in vals])
        # if peaks:
        #     [plt.axvline(p, c='C3', linewidth=2, ls='--') for p in peaks[i-1]]
        i+=1
    plt.tight_layout()
    fig2.savefig(f'Images\Suture\{filename}Suture_Height.png')




#################################################################################################
#################################################################################################
#################################################################################################


# Trajectory for Incision

def Incision_Trajectory(incision_data, filename=''):
    
    fig = plt.figure(figsize=(20,10))
    fig.suptitle(f'{filename} Incision 2D trajectory', fontsize=20)
    x_lines4=[7.2,7.2]
    y_lines4=[11,22]
    i=1
    for data_pos in incision_data:
        ax=fig.add_subplot(2,3,i)
        plt.plot(data_pos['x1'], data_pos['y1'],   color="maroon", linewidth="2",zorder=4)
        plt.xlabel('x[cm]', fontsize=20)
        plt.ylabel('y[cm]', fontsize=20)
        triangle1 = Rectangle( (6.2,11), 2, 11, fc=(0.5,0.3,1,0.5), ec=(0,0,0,0), lw=2,zorder=2)
        triangle2=Rectangle((0,11),14,11,color="pink",zorder=1) 
        plt.plot(x_lines4, y_lines4, color="pink", lw=2,zorder=3)
        ax.add_artist(triangle1)
        ax.add_artist(triangle2)
        plt.xlim([-1,15])
        plt.ylim([10,23])
        plt.rc('axes', titlesize=22)     # fontsize of the axes title
        plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
        plt.rc('legend', fontsize=20)    # legend fontsize
        #plt.grid()
        i+=1
    plt.tight_layout()
    fig.savefig(f'Images\Incision\{filename}_Incision_2D_Trajectory.png')


# Trajectory for Rings

def Rings_Trajectory(rings_data, filename=''):

    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle(f'{filename} Rings 2D trajectory', fontsize=20)
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
        plt.xlabel('x[cm]', fontsize=20)
        plt.ylabel('y[cm]', fontsize=20)
        plt.xlim([-1,22])
        plt.ylim([-1,21])
        plt.rc('axes', titlesize=22)     # fontsize of the axes title
        plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
        plt.rc('legend', fontsize=20)    # legend fontsize
        #plt.grid()
        count+=1
    plt.tight_layout()
    fig2.savefig(f'Images\Rings\{filename}_Rings_2D_Trajectory.png')


# Trajectory for Suture

def Suture_Trajectory(suture_data, filename=''):

    x_spheres=[8,8,13.5,13.5]
    y_spheres=[4,10,4.5,10.5]
    fig3 = plt.figure(figsize=(20,10))
    fig3.suptitle(f'{filename} Suture 2D trajectory', fontsize=20)
    count=1
    for data_pos in suture_data:
        ax=fig3.add_subplot(2,4,count)
        triangle2=Rectangle((0,0),10,16.5,color="pink",zorder=1) 
        triangle3=Rectangle((10.5,0),10,16.5,color="pink",zorder=1) 
        plt.plot(data_pos['x1'], data_pos['y1'],   color="maroon", linewidth="2",zorder=2)
        plt.scatter(x_spheres, y_spheres, s=200, color="red",zorder=3)
        ax.add_artist(triangle2)
        ax.add_artist(triangle3)
        plt.xlim([-1,22])
        plt.ylim([-1,17.5])
        plt.xlabel('x[cm]', fontsize=20)
        plt.ylabel('y[cm]', fontsize=20)
        #plt.grid()
        plt.rc('axes', titlesize=22)     # fontsize of the axes title
        plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
        plt.rc('legend', fontsize=20)    # legend fontsize
        count+=1
    plt.tight_layout()
    fig3.savefig(f'Images\Suture\{filename}_Suture_2D_Trajectory.png')


#################################################################################################
#################################################################################################
#################################################################################################

# Metrics per user (wrt rep and age): scatter and line

def Metrics_Per_User(data,task,title):
    if task=='Suture':
        x_axis=[1,2,3,4,5,6,7,8]
        val1=1
        val2=6
        color1=iter(cm.rainbow(np.linspace(0, 2, 15)))
        color2=iter(cm.rainbow(np.linspace(0, 2, 15)))  
        range_val=7 
    else:
        x_axis=[1,2,3,4,5,6]
        val1=0
        val2=8
        color1=iter(cm.rainbow(np.linspace(0, 2, 16)))
        color2=iter(cm.rainbow(np.linspace(0, 2, 16))) 
        range_val=8   

    fig = plt.figure(figsize=(20,10))
    #fig.suptitle(f'{task} 3D path length wrt repetitions', fontsize=20)

    for user in range(range_val):
        c = next(color1)
        plt.plot(x_axis, data[user],  color=c, linewidth="2", label=f's{user+val1}')
    for user in range(range_val,(len(data))):
        c = next(color2)
        plt.plot(x_axis, data[user],  color=c, linestyle="dashed", linewidth="2", label=f'u{user-val2}')
    plt.ylabel(f'{title}', fontsize=20)
    plt.xlabel('Repetitions', fontsize=20)
    #plt.grid()
    plt.legend(loc=1)
    #plt.show()
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\{title}_user.png')



def Metrics_Per_User_Scatter(data,task, title):
    if task=='Suture':
        x_axis=[1,2,3,4,5,6,7,8]
    # elif task=='Incision':
    #     x_axis=[1,2,3]
    else: 
        x_axis=[1,2,3,4,5,6]
    if task=="Suture":
        names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [ 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
        
    else:
        names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]


    fig = plt.figure(figsize=(20,10))
    #fig.suptitle(f'{task} 3D path length wrt repetitions', fontsize=20)
    data=np.array(data)

    for i, name in enumerate(names):
        color = 'royalblue' if surgeons[i] else 'orchid'
        #res_ages[ages[i]] = data[i]
        if name=='s2' or name=='u6':
            marker='o'
        if name=='s6' or name=='u7':
            marker="^"
        if name=='s3' or name=='u5':
            marker='s'
        if name=='s4' or name=='u3':
            marker='p'
        if name=='s7' or name=='u0':
            marker='X'
        if name=='s5' or name=='u4':
            marker='D'
        if name=='s0' or name=='u1':
            marker='d'
        if name=='s1' or name=='u2':
            marker='*'
        ax = plt.subplot(111)
        plt.scatter(x_axis, data[i],  color=color, s=300, marker=marker, label=name)

    plt.xlabel('Repetitions', fontsize=20)
    plt.ylabel(f'{title}', fontsize=20)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #plt.grid()
    plt.legend(loc=9, ncol=8, fontsize=16)
    if title=='Incision maximum deviation along x [cm]' or title=='Rings 3D Path Length [cm]':
        plt.legend(loc=1, ncol=8, fontsize=16)
    #plt.show()
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\{title}_user_scatter.png')



def Metrics_wrt_age(data,task,title):
    colors=iter(cm.rainbow(np.linspace(0, 2, 16)))
    couple_color=[]
    for i in range(8):
        couple_color.append(next(colors))
    if task=="Suture":
        names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [ 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
    else:
        names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]

    fig = plt.figure(figsize=(20,10))
    #fig.suptitle(f'{task} {title} Path Length wrt Age', fontsize=20)
    res_ages = {}
    sut_mean=np.zeros(len(data))
    for i, name in enumerate(names):

        color = 'royalblue' if surgeons[i] else 'orchid'
        #res_ages[ages[i]] = data[i]
        if name=='s2' or name=='u6':
            marker='o'
        if name=='s6' or name=='u7':
            marker="^"
        if name=='s3' or name=='u5':
            marker='s'
        if name=='s4' or name=='u3':
            marker='p'
        if name=='s7' or name=='u0':
            marker='X'
        if name=='s5' or name=='u4':
            marker='D'
        if name=='s0' or name=='u1':
            marker='d'
        if name=='s1' or name=='u2':
            marker='*'
        #for rep in suture_dist_reps[i]:
        sut_mean[i]=sum(data[i])/len(data[i])
        #print("age:", ages[i], " dist:", sut_mean2)
        ax = plt.subplot(111)
        plt.scatter(ages[i], sut_mean[i], color=color,  s=300, marker=marker, label=name)

    m, b = np.polyfit(ages, sut_mean, 1)
    #print("M of the line, in suture, is: ", m)
    plt.plot(ages, m*np.array(ages) + b, color='black')
    #plt.grid()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #plt.legend(loc=2)
    plt.xlabel('Age [years]', fontsize=20)
    plt.ylabel(f'{title}', fontsize=20)
    plt.rc('axes', titlesize=20)     # fontsize of the axes title
    plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    
    plt.legend(loc=9, ncol=8, fontsize=16)
    if title=='Suture 3D Path Length [cm]' or title=='Suture 3D Path Length [cm] Second Part  'or title=='Suture 3D Path Length [cm] First Part  ':
        plt.legend(loc=2, ncol=8, fontsize=16)
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\{title}_Age.png')



#################################################################################################
#################################################################################################
#################################################################################################

# Metrics mean for repetition: barplot and line

def Metrics_Mean_Std_Err_Reps(data,task,title):
    if task=='Suture':
        x_axis=[1,2,3,4,5,6,7,8]
        names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
        nSurgeons=7
        nReps=8
    else:
        x_axis=[1,2,3,4,5,6]
        names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
        nSurgeons=8
        nReps=6
    data=np.array(data)
    fig = plt.figure(figsize=(20,10))
    #fig.suptitle(f'{task} {data_type} wrt repetitions - Mean and Std Dev', fontsize=20)
    surgeon_mean=np.zeros(nReps)
    control_mean=np.zeros(nReps)
    surgeon_std=np.zeros(nReps)
    control_std=np.zeros(nReps)
    for i in range(nReps):
        temp=data[0:nSurgeons,i]
        surgeon_mean[i]=temp.mean()
        
        surgeon_std[i]=temp.std()/np.sqrt(np.size(temp))
        temp2=data[nSurgeons:,i]
        control_mean[i]=temp2.mean()

        control_std[i]=temp2.std()/np.sqrt(np.size(temp))
    plt.plot(x_axis, surgeon_mean,  color="royalblue", linewidth=5, label='Surgeons')
    plt.plot(x_axis, control_mean,  color="orchid", linestyle="dashed", linewidth=5, label='Control')
    plt.errorbar(x_axis, surgeon_mean, yerr=surgeon_std, capsize=10, color="royalblue", linewidth=3, marker='^')
    plt.errorbar(x_axis, control_mean, yerr=control_std,  capsize=10, linestyle="dashed", color="orchid", linewidth=3, marker='^')
    plt.xlabel('Repetitions', fontsize=20)
    plt.ylabel(f'{title}', fontsize=20)
    plt.rc('axes', titlesize=20)     # fontsize of the axes title
    plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    plt.rc('legend', fontsize=20)    # legend fontsize
    #plt.grid()
    plt.legend(loc=1)
    #plt.show()
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\{title}_mean.png')



def Metrics_Mean_Std_Err_Barplot_Reps(data,task,title):
    if task=='Suture':
        x_axis=[1,2,3,4,5,6,7,8]
        names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
        nSurgeons=7
        nReps=8
    else:
        x_axis=[1,2,3,4,5,6]
        names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
        surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
        ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
        nSurgeons=8
        nReps=6
    data=np.array(data)
    fig = plt.figure(figsize=(20,10))
    #fig.suptitle(f'{task} {data_type} wrt repetitions - Mean and Std Dev', fontsize=20)
    surgeon_mean=np.zeros(nReps)
    control_mean=np.zeros(nReps)
    surgeon_std=np.zeros(nReps)
    control_std=np.zeros(nReps)
    for i in range(nReps):
        temp=data[0:nSurgeons,i]
        surgeon_mean[i]=temp.mean()
        surgeon_mean[i]=np.median(temp)
        surgeon_std[i]=temp.std()/np.sqrt(np.size(temp))
        temp2=data[nSurgeons:,i]
        control_mean[i]=temp2.mean()
        control_mean[i]=np.median(temp2)
        control_std[i]=temp2.std()/np.sqrt(np.size(temp))
    plt.bar(x_axis, surgeon_mean, width=-0.3, yerr=surgeon_std, capsize=10, align='edge', color='royalblue', label="Surgeons Group")
    plt.bar(x_axis, control_mean,  width=0.3, yerr=control_std, capsize=10, align='edge', color='orchid', label="Control Group")
    
    plt.xlabel('Repetitions', fontsize=20)
    plt.ylabel(f'{title}', fontsize=20)
    plt.rc('axes', titlesize=20)     # fontsize of the axes title
    plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    plt.rc('legend', fontsize=20)    # legend fontsize
    #plt.grid()
    #if title=='Rings Mean Path Length 2D [cm]' or title=='Rings Mean Path Length 3D [cm]'
    plt.legend(loc=2)
    #plt.show()
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\{title}_mean_bar.png')



def Incision_barplot(data, title):

    names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
    nSurgeons=8
    nOrient=3
    data=np.array(data)
    x_axis=np.array([1,2,3])
    values=[10,25,40]


    surgeon_mean=np.zeros(nOrient)
    control_mean=np.zeros(nOrient)
    surgeon_std=np.zeros(nOrient)
    control_std=np.zeros(nOrient)
    fig = plt.figure(figsize=(20,10))
    #fig.suptitle(f'Incision wrt orient', fontsize=20)
    counter=0
    for i in [0,2,4]:
        # print("Total rows:", data)
        temp=data[0:nSurgeons,i:i+2]
        # print(f"Rows {i}:",  temp)
        surgeon_mean[counter]=temp.mean()
        surgeon_std[counter]=temp.std()/np.sqrt(np.size(temp))
        temp2=data[nSurgeons:,i:i+2]
        control_mean[counter]=temp2.mean()
        control_std[counter]=temp2.std()/np.sqrt(np.size(temp))
        counter+=1
    plt.bar(x_axis, surgeon_mean, width=-0.3, yerr=surgeon_std, capsize=10, align='edge', color='royalblue', label="Surgeons Group")#, alpha=0.5, ecolor='black', capsize=10)
    plt.bar(x_axis, control_mean, width=0.3, yerr=control_std, capsize=10, align='edge', color='orchid', label="Control Group")#, alpha=0.5, ecolor='black', capsize=10)
    plt.xlabel('Orientation along the z axis [$^\circ$]', fontsize=20)
    plt.ylabel(f'{title}', fontsize=20)
    plt.xticks(x_axis,values)
    plt.legend(loc=1, fontsize=20)
    plt.tight_layout()
    #plt.rc('legend', fontsize=20)    # legend fontsize
    fig.savefig(f'Data\Metrics - Single User\{title}_wrt_orientation.png')    



#################################################################################################
#################################################################################################
#################################################################################################



def Handle_Suture(suture_data,filename):
    
    # rep_first_chunck=[]
    # rep_second_chunck=[]
    peaks1=[]
    peaks2=[]
    tot_dist_reps1=[]
    tot_dist_reps2=[]
    fig3 = plt.figure(figsize=(20,10))
    fig3.suptitle(f'{filename} Suture 2D trajectory', fontsize=20)   
    Path_Length_Total1=[]
    Path_Length_Total2=[]
    print("hei")
    for i, rep in enumerate(suture_data):

        x = rep['x1'].values
        y = rep['y1'].values
        z = rep['z1'].values
        x_spheres=[8,8,13.5,13.5]
        y_spheres=[4,10,4.5,10.5]
        third_sph=np.where((x<15)&(x>12)&(y<6)&(y>2.5))[0]
        final=-1 # Data is clean already
        second_sph=np.where((x<10)&(x>6)&(y<12)&(y>8))[0]
        if second_sph!=[]:
            cut_index_0=second_sph[-1]
        else:
            cut_index_0=(np.where(y<6)[0][0])

        if third_sph!=[]:
            cut_index=third_sph[0]#[int(len(third_sph)/2)]
            if cut_index<=cut_index_0:
                cut_index=third_sph[-1]
        else:
            cut_index=1
            print('Error!!!!!!!!!!!!!!!!!!!!!!111')
        if filename=='s3' and i==4:
            final=(np.where((x<9)&(x>5)&(y<5)&(y>3))[0][0])+1
        if filename=='s4' and i==5:
            final=(np.where((x<9)&(x>5)&(y<5)&(y>3))[0][0])+1
        if filename=='u1' and i==1:
            final=(np.where((x<9)&(x>5)&(y<5)&(y>3))[0][-1])+1
        if filename=='s2' and i==2:
            final=(np.where((x<9)&(x>5)&(y<5)&(y>3))[0][-1])+1
            cut_index_0=second_sph[-5]
        if filename=='u7' and i==2:
            cut_index=(np.where(y<6)[0][0])+1
        if filename=='u7' and i==0:
            cut_index=int(len(x)/2)+10
            cut_index_0=int(len(x)/2)-10
        if filename=='u2':
            cut_index_0=second_sph[int(len(second_sph)/2.5)]
        if filename=='u6' and i==6:
            cut_index_0=second_sph[int(len(second_sph)/2)]
            final=final-16


        x1=x[0:cut_index_0+1]
        x2=x[cut_index-1:final]
        y1=y[0:cut_index_0+1]
        y2=y[cut_index-1:final]
        z1=y[0:cut_index_0+1]
        z2=y[cut_index-1:final]

        ax=fig3.add_subplot(2,4,i+1)
        triangle2=Rectangle((0,0),10,16.5,color="pink",zorder=1) 
        triangle3=Rectangle((10.5,0),10,16.5,color="pink",zorder=1) 
        ax.add_artist(triangle2)
        ax.add_artist(triangle3)
        plt.plot(x1, y1,   color="maroon", linewidth="2",zorder=2)
        plt.plot(x2, y2,   color="blue", linewidth="2",zorder=2)
        plt.scatter(x_spheres, y_spheres, s=300, color="red",zorder=3)
        #plt.scatter(rep['x1'].values[third_sph], rep['y1'].values[third_sph], s=100, color="blue",zorder=4)
        # ax.add_artist(triangle2)
        # ax.add_artist(triangle3)
        plt.xlim([-1,22])
        plt.ylim([-1,17.5])
        plt.xlabel('x[cm]', fontsize=20)
        plt.ylabel('y[cm]', fontsize=20)
        #plt.grid()
        plt.rc('axes', titlesize=22)     # fontsize of the axes title
        plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
        plt.rc('legend', fontsize=20)    # legend fontsize

        
        #peaks1.append(len(find_peaks(z1)[0]))
        #peaks2.append(len(find_peaks(z2)[0]))
        dist=[]
        points1=list(zip(x1,y1,z1))
        for i in range(len(x1)):
            dist.append(distance.euclidean( points1[i],points1[i-1] )  )
        tot_dist1=sum(dist)
        tot_dist_reps1.append(tot_dist1)
        dist=[]
        points2=list(zip(x2,y2,z2))
        for i in range(len(x2)):
            dist.append(distance.euclidean( points2[i],points2[i-1] )  )
        tot_dist2=sum(dist)
        tot_dist_reps2.append(tot_dist2)
    
    # print(tot_dist_reps1)
    # print(tot_dist_reps2)
    plt.tight_layout()
    fig3.savefig(f'Images\Suture\{filename}_Suture_2D_Trajectory_2Parts.png')


    return [tot_dist_reps1,tot_dist_reps2]

    

def SutPL12(suture_data):
    fig = plt.figure(figsize=(20,10))
    fig.suptitle(f'Suture divided in 2', fontsize=20)    
    x_axis=[1,2,3,4,5,6,7,8]
    names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
    #print("all: ",suture_data)
    Path_Length_Total1=[]
    Path_Length_Total2=[]
    for i, element in enumerate(suture_data[1:]):
        #print("user ", element)
        element=np.array(element)
        PL1=element[0]
        PL2=element[1]
        Path_Length_Total1.append(PL1)
        Path_Length_Total2.append(PL2)

    Metrics_Per_User(Path_Length_Total1, 'Suture', 'Suture 3D Path Length [cm] First Part')
    Metrics_Per_User(Path_Length_Total2, 'Suture', 'Suture 3D Path Length [cm] Second Part')
    Metrics_Per_User_Scatter(Path_Length_Total1, 'Suture', 'Suture 3D Path Length [cm] First Part')
    Metrics_Per_User_Scatter(Path_Length_Total2, 'Suture', 'Suture 3D Path Length [cm] Second Part')
    Metrics_Mean_Std_Err_Reps(Path_Length_Total1, 'Suture', 'Suture 3D Path Length [cm] First Part')
    Metrics_Mean_Std_Err_Reps(Path_Length_Total2, 'Suture', 'Suture 3D Path Length [cm] Second Part')
    Metrics_Mean_Std_Err_Barplot_Reps (Path_Length_Total1, 'Suture', 'Suture 3D Path Length [cm] First Part')
    Metrics_Mean_Std_Err_Barplot_Reps(Path_Length_Total2, 'Suture', 'Suture 3D Path Length [cm] Second Part')
    Metrics_wrt_age(Path_Length_Total1, 'Suture', 'Suture 3D Path Length [cm] First Part')
    Metrics_wrt_age(Path_Length_Total2, 'Suture', 'Suture 3D Path Length [cm] Second Part')
    Metrics_Mean_Std_Err_Reps_Sut(Path_Length_Total1, Path_Length_Total2, 'Suture 3D Path Length [cm] Both parts')




def Metrics_Mean_Std_Err_Reps_Sut(data1, data2,title):

    x_axis=np.array([1,2,3,4,5,6,7,8])
    names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
    nSurgeons=7
    nReps=8
    fig = plt.figure(figsize=(20,10))    
    data1=np.array(data1)
    #fig.suptitle(f'{task} {data_type} wrt repetitions - Mean and Std Dev', fontsize=20)
    surgeon_mean=np.zeros(nReps)
    control_mean=np.zeros(nReps)
    surgeon_std=np.zeros(nReps)
    control_std=np.zeros(nReps)
    for i in range(nReps):
        temp=data1[0:nSurgeons,i]
        surgeon_mean[i]=temp.mean()
        surgeon_mean[i]=np.median(temp)
        surgeon_std[i]=temp.std()/np.sqrt(np.size(temp))
        temp2=data1[nSurgeons:,i]
        control_mean[i]=temp2.mean()
        control_mean[i]=np.median(temp2)
        control_std[i]=temp2.std()/np.sqrt(np.size(temp))
    plt.bar(x_axis-0.4, surgeon_mean, width=0.2, yerr=surgeon_std, capsize=10, align='edge', color='royalblue', label="Surgeons Group First Part")
    plt.bar(x_axis-0.2, control_mean,  width=0.2, yerr=control_std, capsize=10, align='edge', color='orchid', label="Control Group First Part")
    data2=np.array(data2)
    #fig.suptitle(f'{task} {data_type} wrt repetitions - Mean and Std Dev', fontsize=20)
    surgeon_mean=np.zeros(nReps)
    control_mean=np.zeros(nReps)
    surgeon_std=np.zeros(nReps)
    control_std=np.zeros(nReps)
    for i in range(nReps):
        temp=data2[0:nSurgeons,i]
        surgeon_mean[i]=temp.mean()
        surgeon_mean[i]=np.median(temp)
        surgeon_std[i]=temp.std()/np.sqrt(np.size(temp))
        temp2=data2[nSurgeons:,i]
        control_mean[i]=temp2.mean()
        control_mean[i]=np.median(temp2)
        control_std[i]=temp2.std()/np.sqrt(np.size(temp))
    plt.bar(x_axis, surgeon_mean, width=0.2, yerr=surgeon_std, capsize=10, align='edge', color='cornflowerblue', label="Surgeons Group First Part")
    plt.bar(x_axis+0.2, control_mean,  width=0.2, yerr=control_std, capsize=10, align='edge', color='plum', label="Control Group First Part")
    plt.xlabel('Repetitions', fontsize=20)
    plt.ylabel(f'{title}', fontsize=20)
    plt.xticks(x_axis)
    plt.rc('axes', titlesize=20)     # fontsize of the axes title
    plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    plt.rc('legend', fontsize=20)    # legend fontsize
    #plt.grid()
    plt.legend(loc=2)
    #plt.show()
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\Suture {title}.png')












def Mean_Std_Dev_Sut_peaks(data):
    x_axis=[1,2,3,4,5,6,7,8]
    names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]
    nSurgeons=7
    nReps=8
    data=np.array(data)
    print(data)

    fig = plt.figure(figsize=(20,10))
    fig.suptitle(f'Suture peaks wrt repetitions - Mean and Std Dev', fontsize=20)
    surgeon_mean=np.zeros(nReps)
    control_mean=np.zeros(nReps)
    surgeon_std=np.zeros(nReps)
    control_std=np.zeros(nReps)
    print(data)
    print(data[0])
    #print(data[0:2, 0][0])
    for i in range(nReps):
        temp=data[0:nSurgeons,i]
        temp2=data[nSurgeons:,i]
        surgeon_mean1[i]=temp[0].mean()
        surgeon_std1[i]=temp[0].std()/np.sqrt(np.size(temp))
        control_mean1[i]=temp2[0].mean()
        control_std1[i]=temp2[0].std()/np.sqrt(np.size(temp))

        surgeon_mean2[i]=temp[1].mean()
        surgeon_std2[i]=temp[1].std()/np.sqrt(np.size(temp))
        control_mean2[i]=temp2[1].mean()
        control_std2[i]=temp2[1].std()/np.sqrt(np.size(temp))

    plt.plot(x_axis, surgeon_mean1,  color="royalblue", linewidth="3", label='Surgeons1')
    plt.plot(x_axis, control_mean1,  color="orchid", linestyle="dashed", linewidth="3", label='Control1')
    plt.plot(x_axis, surgeon_mean2,  color="pink", linewidth="3", label='Surgeons2')
    plt.plot(x_axis, control_mean2,  color="green", linestyle="dashed", linewidth="3", label='Control2')

    # plt.errorbar(x_axis, surgeon_mean, yerr=surgeon_std, color="royalblue",  marker='^')
    # plt.errorbar(x_axis, control_mean, yerr=control_std, linestyle="dashed", color="orchid",  marker='^')
    plt.xlabel('Repetitions', fontsize=20)
    plt.ylabel(f'Number Peaks', fontsize=20)
    plt.rc('axes', titlesize=20)     # fontsize of the axes title
    plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    plt.rc('legend', fontsize=20)    # legend fontsize
    #plt.grid()
    plt.legend(loc=1)
    #plt.show()
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\Suture_peaks.png')