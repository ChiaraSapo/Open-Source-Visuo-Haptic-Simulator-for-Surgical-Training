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

# Write path to the Folder containing each subject's data
subjects_path='C:\\Users\\chiar\\OneDrive\\Desktop\\Subjects'

## Choose what to compute/plot:
# Plot graphs of incision, rings and suture
plot_incision=True
plot_rings=True
plot_suture=True
# Compute metrics: path length, peaks, mean distance....
compute_metrics=True
# Plot metrics for each user
plot_metrics_per_user=False

# Data for the metrics
incision_dist_reps=[]
incision_dist_7=[]
incision_dist_1_5=[]
suture_dist_reps=[]
rings_dist_reps=[]
total_peaks=[]
traj_in_boxes = []

NSurgeons = 0
NControl = 0

# Look for all folders and files in specified subjects path
for folder in os.listdir(subjects_path):

    # If "folder" is actually a folder
    if os.path.isdir(subjects_path + '\\' + folder) and not 'Images' in folder and not 'chache' in folder and not 'Data' in folder:# and not 'u7' in folder: # U7 da problemi
    
        incision_data = []
        rings_data = []
        suture_data = []
        incision_peaks = []
        rings_peaks = []
        #suture_peaks = []
        
        path =  subjects_path + f'\\{folder}' 

        if 's' in folder:
            NSurgeons +=1
        if 'u' in folder:
            NControl += 1
        
        # Look for all files inside the subject folder
        for filename in os.listdir(path):
            

            # INCISION FILES (Positional data)
            if (plot_incision==True or compute_metrics==True) and 'Incision' in filename and 'Pos' in filename and filename.endswith('.txt'):
                # Save type of orientation (2-3-4)
                orientation_id = filename.split('Incision')[1][0]
                # Read csv file with positional data
                df = pd.read_csv(path + '\\' + filename, skiprows=[0, 1], engine='python', index_col=False,
                                 delim_whitespace=True,
                                 names=['Time', 'x1', 'y1', 'z1'])

                # Save x,y,z data
                x = df['x1'].values
                y = df['y1'].values
                z = df['z1'].values

                # Save "good" points, i.e. the ones in the skin range 
                good = np.where((x <= 8) & (x >= 6) & (y <= 22) & (y >= 10) & (z <= 3) & (z >= -1))[0]

                # Set the min y coordinate as the minimum of the y(t)
                last=np.argmin(y)

                # Save values from the first time the user was in the right position over the skin for the first time, 
                # to the last point as defined before
                df_filtered = df.loc[good[0]: last, :]

                # Smooth the height to count peacks better
                df_filtered['z1'] = df_filtered['z1'].rolling(100).mean()

                # Save all these modified values are incision data to plot
                incision_data.append(df_filtered)

                # Find indices of the peaks in the height
                p = find_peaks(df_filtered['z1'], prominence=1)

                # Find the corrensponding time instant of the peaks
                incision_peaks.append(df_filtered['Time'].values[p[0]])




            # RINGS FILES (Positional data)
            if (plot_rings==True or compute_metrics==True) and 'Rings' in filename and 'Pos' in filename and filename.endswith('.txt'):

                # Read csv file with positional data
                df = pd.read_csv(path + '\\' + filename, skiprows=[0, 1], engine='python', index_col=False,
                                 delim_whitespace=True,
                                 names=['Time', 'x1', 'y1', 'z1'])

                # Save x,y,z data
                x = df['x1'].values
                y = df['y1'].values
                z = df['z1'].values

                # Save "good" points, i.e. the ones in the skin range 
                good = np.where((x <= 21) & (x >= 0) & (y <= 20) & (y >= 0) & (z <= 15) & (z >= -0.5))[0]
                idx = np.where( (y<=4.9) & (x<=7.5) & (x>=5.5))[0]
                
                if idx!=[]:
                    last=idx[0]
                else:
                    i = 2
                    while int(y[-i]) <= int(y[-i + 1]):  # Possibly add patience
                        i += 1
                    last = len(y) - i

                # Save values from the first time the user was in the right position over the skin for the first time, 
                # to the last point as defined before
                df_filtered = df.loc[good[0]: min(last, good[-1]), :]

                # Smooth the height to count peacks better
                df_filtered['z1'] = df_filtered['z1'].rolling(50).mean()

                # Save all these modified values are rings data to plot
                rings_data.append(df_filtered)

                # Find indices of the peaks in the height
                p = find_peaks(-df_filtered['z1'], prominence=1) # Minus to find neg peaks, prominence singe centers are at z=4
                
                # Desired peaks
                p2 = []

                for peak in p[0]:
                    if df_filtered['z1'].values[peak] <=2.5: # Take only the ones that touch the skin (?)
                        p2.append(peak)

                # Find the corrensponding time instant of the peaks
                rings_peaks.append(df_filtered['Time'].values[p2])

                # Data for metrics
                total_peaks.append(p2)

 



            # SUTURE FILES (Positional data)
            if (plot_suture==True or compute_metrics==True) and 'Suture' in filename and 'Pos' in filename and filename.endswith('.txt') :

                # Read csv file with positional data
                df = pd.read_csv(path + '\\' + filename, skiprows=[0, 1], engine='python', index_col=False,
                                delim_whitespace=True,
                                names=['Time', 'x1', 'y1', 'z1'])
                # Save x,y,z data
                x = df['x1'].values
                y = df['y1'].values
                z = df['z1'].values

                # Save "good" points, i.e. the ones in the skin range 
                good = np.where((x <= 20.5) & (x >= 0) & (y <= 16.5) & (y >= 0) & (z <= 10) & (z >= -1))[0]
                idx = np.where( (y<=4.5) & (x>=3.5) & (x>=6.5) & (x<=9.5))[0]
            
                if idx!=[]:
                    last=idx[-1]
                else:
                    i = 2
                    while int(y[-i]) <= int(y[-i + 1]):  # Possibly add patience
                        i += 1
                    last = len(y) - i


                # Save values from the first time the user cut the skin for the first time, or at least touched it in the right position
                df_filtered = df.loc[good[0]: min(last, good[-1]), :]

                # Smooth the height to count peacks better
                df_filtered['z1'] = df_filtered['z1'].rolling(50).mean()

                # Save all these modified values are suture data to plot
                suture_data.append(df_filtered)

                # Find indices of the peaks in the height (Removed for now)
                # p = find_peaks(df_filtered['z1'], prominence=1)



        # Plot trajectory and height for all tasks
        if plot_incision==True:
            Handle_data.Incision_Height(incision_data, incision_peaks, filename=folder)
            Handle_data.Incision_Trajectory(incision_data, folder)

        if plot_rings==True:
            Handle_data.Rings_Height(rings_data, rings_peaks, filename=folder)
            Handle_data.Rings_Trajectory(rings_data, filename=folder)

        if plot_suture==True:
            Handle_data.Suture_Height(suture_data, filename=folder)
            Handle_data.Suture_Trajectory(suture_data, filename=folder)

        # Compute metrics for all tasks
        if compute_metrics==True:
            
            # Save values for pandas dataframes 
            traj_in_boxes.append(Handle_data.Suture_Path_Length_per_user_wrt_peaks(suture_data))
            suture_dist_reps.append(Handle_data.Suture_Path_Length_per_user(suture_data))
            incision_dist_reps.append(Handle_data.Incision_Path_Length_per_user(incision_data))
            incision_dist_7.append(Handle_data.Incision_Path_Length_per_user_from_7(incision_data))
            incision_dist_1_5.append(Handle_data.Incision_Path_Length_per_user_from_1_5(incision_data))
            rings_dist_reps.append(Handle_data.Rings_Path_Length_per_user(rings_data))
                  

        # Uncomment to have first subject only 
        # break


if plot_metrics_per_user==True:

    # Plot metrics values for each user
    Handle_data.Incision_Path_Length_plot_per_user(incision_dist_reps, NSurgeons=8, NControl=8)
    Handle_data.Incision_Path_Length_plot_per_user_from_7(incision_dist_7, NSurgeons=8, NControl=8)
    Handle_data.Incision_Path_Length_plot_per_user_from_1_5(incision_dist_1_5, NSurgeons=8, NControl=8)
    Handle_data.Rings_Path_Length_plot_per_user(rings_dist_reps, NSurgeons=8, NControl=8)
    Handle_data.Suture_Path_Length_plot_per_user(suture_dist_reps, NSurgeons=8, NControl=8)     


if compute_metrics==True:

    Handle_data.Data_Rings_Peaks(total_peaks)
    Handle_data.Data_Suture_Box(traj_in_boxes)
    Handle_data.Data_total(incision_dist_reps, suture_dist_reps, rings_dist_reps, incision_dist_7, incision_dist_1_5)


