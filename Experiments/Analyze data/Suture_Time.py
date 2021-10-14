import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import numpy as np
from scipy.interpolate import interp2d
from scipy.signal import find_peaks
import Handle_data
import os
import seaborn as sns
from scipy.stats import pointbiserialr
import scipy 
from scipy.spatial import distance
import math
from matplotlib.pyplot import cm


def suture_time_computation():
    # Write path to the Folder containing each subject's data
    subjects_path='C:\\Users\\chiar\\OneDrive\\Desktop\\Subjects'

    NControl = 0
    NSurgeons = 0
    file_length = []
    time_file_length = []

    ################### Count subjects ########################

    # # Look for all folders and files in specified subjects path
    # for folder in os.listdir(subjects_path):

    #     # If "folder" is actually a folder
    #     if os.path.isdir(subjects_path + '\\' + folder) and not 'Images' in folder and not 'chache' in folder and not 'Data' in folder:# and not 'u7' in folder: # U7 da problemi

    #         if 's' in folder or 'S' in folder:
    #             NSurgeons +=1
    #         if 'u' in folder:
    #             NControl += 1

    # Ntot=NSurgeons+NControl
    # print("Surgeons: ", NSurgeons, " Control: ", NControl)


    ################### Compute suture time ########################
    suture_period_user=[]
    suture_time=[]
    total_time=[]
    for folder in os.listdir(subjects_path):

        # If "folder" is actually a folder
        if os.path.isdir(subjects_path + '\\' + folder) and not 'Images' in folder and not 'chache' in folder and not 'Data' in folder and not 'S0' in folder and not 'u0' in folder:# and not 'u7' in folder: # U7 da problemi

            path =  subjects_path + f'\\{folder}'
            user_time_file_length = []

            if ('s' in folder or 'u' in folder or 'S' in folder) and 'u0' not in folder and 'S0' not in folder:

                user_time=np.zeros(8)
                #print(folder)
                with open(f'{path}\\Sut.txt') as f:
                    lines = f.readlines()
                    text = ''.join(lines).strip()
                    groups = text.split('\n\n')
                    result = []
                    if  folder == 'S1':
                        #groups[1]=groups[1][331:] DO LATER
                        groups=groups[1:-3]
                    if folder=="s5":
                        groups=groups[2:]
                    else:
                        groups=groups[1:]
                    for g in groups:
                        array = np.array(g.strip().split('\n'))
                        result.append([float(x) for x in array])
                        user_time_file_length.append(len(array))
                    total_time.append(result)

                        
                time_file_length.append(user_time_file_length)
                


                for i in range(1,len(result)):
                    user_time[i-1]=(result[i][-1]-result[i-1][0])

                suture_time.append(user_time)

                temp_period=[]
                for a in range(len(result)):
                    for b in range(1,len(result[a])):
                        temp_period.append(result[a][b]-result[a][b-1])
                suture_period_user.append(temp_period)
                #print("User", folder, ", time length:", user_time_file_length)


    suture_freq=[]
    suture_period=[]
    for T in suture_period_user:
        for element in T:
            suture_freq.append(1/element)
            suture_period.append(element)

    print("Min freq:", min(suture_freq), ". Max freq:", max(suture_freq), ". Mean freq: ", sum(suture_freq)/len(suture_freq))
    print("Min period:", min(suture_period), ". Max period:", max(suture_period), ". Mean period: ", sum(suture_period)/len(suture_period))

    # Delta_max=max(suture_period)




    # ################### Retrieve subjects data ########################

    person=0

    indices=np.zeros([14,8,2])


    for folder in os.listdir(subjects_path):

        # If "folder" is actually a folder
        if os.path.isdir(subjects_path + '\\' + folder) and not 'Images' in folder and not '__' in folder and not 'Data' in folder and not 'S0' in folder and not 'u0' in folder:# and not 'u7' in folder: # U7 da problemi
            count=1
            fig = plt.figure(figsize=(20,10))
            fig.suptitle(f'Suture Vel for subject {folder}', fontsize='x-large') 
            incision_data = []
            rings_data = []
            suture_data = []
            incision_peaks = []
            rings_peaks = []

            path =  subjects_path + f'\\{folder}'

            # print(folder)
            user_file_length=[]
            if 'S0' and 'u0' not in folder: # S0 cannot be counted in Suture
                
                repetitions=0

                # Look for all files inside the subject folder
                for filename in os.listdir(path):
                    

                    # SUTURE FILES (Positional data)
                    if 'Suture' in filename and 'Pos' in filename and filename.endswith('.txt') :
                        
                    
                    
                        #print(filename)

                        # Read csv file with positional data
                        df = pd.read_csv(path + '\\' + filename, skiprows=[0, 1], engine='python', index_col=False,
                                        delim_whitespace=True,
                                        names=['Time', 'x1', 'y1', 'z1'])
                        # Save x,y,z data
                        x = df['x1'].values
                        y = df['y1'].values
                        z = df['z1'].values

                        
                        user_file_length.append(len(df['Time']))

                        # Save "good" points, i.e. the ones in the skin range
                        good_suture = np.where((x <= 20.5) & (x >= 0) & (y <= 16.5) & (y >= 0) & (z <= 10) & (z >= -1))[0]
                        idx = np.where( (y<=4.5) & (x>=3.5) & (x>=6.5) & (x<=9.5))[0]

                        if idx.size!=0:
                            last_suture=idx[-1]
                        else:
                            i = 2
                            while int(y[-i]) <= int(y[-i + 1]):  # Possibly add patience
                                i += 1
                            last_suture = len(y) - i
                        #print(good_suture[0])
                        indices[person,repetitions,0]=good_suture[0]
                        indices[person,repetitions,1]=min(last_suture, good_suture[-1])
                        repetitions+=1
                        
                        df_filtered = df.loc[good_suture[0]: min(last_suture, good_suture[-1]), :]
                        suture_data.append(df_filtered)


                # if 'Suture' in filename and 'Vel' in filename and filename.endswith('.txt'):
                #     #print(filename)
                #     if 'S0' and 'u0' not in folder: # S0 cannot be counted in Suture
                #         df = pd.read_csv(path + '\\' + filename, skiprows=[0, 1], engine='python', index_col=False,
                #                         delim_whitespace=True,
                #                         names=['Time', 'x1', 'y1', 'z1'])
                #         df2=df.loc[good_suture[0]: last_suture, :]
                #         df_filtered=scipy.signal.savgol_filter(x=df2['z1'], window_length=5, polyorder=4, deriv=1, delta= Delta_max)#, delta=1.0, axis=- 1, mode='interp', cval=0.0)

                #         ax=fig.add_subplot(2,4,count)
                #         plt.plot(df2['Time'], df_filtered, color="maroon", linewidth="2",zorder=2)
                #         plt.xlabel('Time[dt]', fontsize='x-large')
                #         plt.ylabel('Vel[cm/s]', fontsize='x-large')
                #         plt.grid()
                #         plt.tight_layout()
                #         fig.savefig(f'{folder}_Suture_Vel.png')
                #         count+=1


    # Cut real time
    person=0
    rep=0

    period=np.zeros([14,8,2])
    #print("Time from files has dim:", len(total_time),"x",len(total_time[0]))


    # for i in range(14): #per user
    #     for j in range(8): #per rep
    #         temp=total_time[i][j]
    #         temp=temp[int(indices[i][j][0]):int(indices[i][j][1]) ]
    #         print(i,j)
    #         period[i,j,0]=temp[0]
    #         period[i,j,1]=temp[1]
    #         total_time[i][j]=temp

    total_period=[]
    for i in range(14): #per user
        for j in range(8): #per rep
            temp=total_time[i][j]
            for k in (1,total_time[i][j]):
                #print(temp[i], temp[i-1])
                total_period.append(temp[i]-temp[i-1])
    print("Min Period: ", min(total_period), ", Max Period: ", max(total_period))#, ", Mean: ", sum(period)/len(period))

    # time_file_length[4]=time_file_length[4][1:]
    # time_file_length[0]=time_file_length[0][1:-3]
    names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u1", "u2", "u3", "u4", "u5", "u6", "u7"]

    #for i in range(len(file_length)):
        #print("User", names[i], " position len:", file_length[i], " and time len:", time_file_length[i])


    rep1=[]
    rep2=[]
    rep3=[]
    rep4=[]
    rep5=[]
    rep6=[]
    rep7=[]
    rep8=[]

    for user in range(len(total_time)):
        temp=total_time[user]
        rep1.append(temp[0][-1]-temp[0][0])
        rep2.append(temp[1][-1]-temp[1][0])
        rep3.append(temp[2][-1]-temp[2][0])
        rep4.append(temp[3][-1]-temp[3][0])
        rep5.append(temp[4][-1]-temp[4][0])
        rep6.append(temp[5][-1]-temp[5][0])
        rep7.append(temp[6][-1]-temp[6][0])
        rep8.append(temp[7][-1]-temp[7][0])


    fig = plt.figure(figsize=(20,10))
    fig.suptitle('Time in suture', fontsize='x-large')
    user=0
    #print([rep1[user],rep2[user],rep3[user],rep4[user], rep5[user],rep6[user],rep7[user],rep8[user]])

    color = iter(cm.rainbow(np.linspace(0, 2, 16)))
    for user in range(7):
        c = next(color)
        plt.plot([1,2,3,4,5,6,7,8], [rep1[user],rep2[user],rep3[user],rep4[user], rep5[user],rep6[user],rep7[user],rep8[user]] , color=c, linewidth="2", label=f's{user+1}')
    color = iter(cm.rainbow(np.linspace(0, 2, 16)))
    for user in range(7,14):
        c = next(color)
        plt.plot([1,2,3,4,5,6,7,8], [rep1[user],rep2[user],rep3[user],rep4[user], rep5[user],rep6[user],rep7[user],rep8[user]] ,  color=c, linestyle="dashed", linewidth="2", label=f'u{user-6}')

    plt.xlabel('Repetitions', fontsize='x-large')
    plt.ylabel('Time [s]', fontsize='x-large')
    plt.grid()
    plt.legend()
    #plt.show()
    plt.tight_layout()
    fig.savefig(f'Data\Metrics - Single User\Suture_Time.png')

    total_suture_time=[]
    for user in range(14):
        total_suture_time.append([rep1[user],rep2[user],rep3[user],rep4[user], rep5[user],rep6[user],rep7[user],rep8[user]])
    return total_suture_time