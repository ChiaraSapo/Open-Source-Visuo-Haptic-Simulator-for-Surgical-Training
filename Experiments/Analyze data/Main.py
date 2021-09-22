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

# Choose what you want to plot
plot_incision=False#True
plot_rings=True#False#True
plot_suture=False#True
compute_metrics=False

# Data for the metrics
incision_dist_reps=[]
incision_dist_7=[]
incision_dist_1_5=[]
suture_dist_reps=[]
rings_dist_reps=[]
total_peaks=[]

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

                # Look for the return, by starting from the end and making a good approx by working with integers:
                # loop until values are decreasing in time (going back towards the Geomagic Touch)
                # y_rev = np.flip(y)
                # patience = 0
                # for i in range(len(y)-1):
                #     if int(y_rev[i]) >= int(y_rev[i+1]):
                #         patience = 0
                #         if i == np.argmin(y_rev):
                #             break
                #         else:
                #             continue
                #     else:
                #         patience += 1
                #         if patience >= 350 or i == np.argmin(y_rev):
                #             break

                # last = len(y) - i + patience

                # Save values from the first time the user cut the skin for the first time, or at least touched it in the right position
                #df_filtered = df.loc[good[0]: min(last, good[-1]), :]

                # Set the min y coordinate as the last point
                last=np.argmin(y)
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


                # Save values from the first time the user cut the skin for the first time, or at least touched it in the right position
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

                if 'S0' not in folder: # S0 cannot be counted in Suture

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
                    #first = np.where((x <= 15.5) & (x >= 11.5) & (y <= 12.5) & (y >= 8.5) & (z <= 20) & (z >= -1))[0]
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

                    # Find indices of the peaks in the height
                    p = find_peaks(df_filtered['z1'], prominence=1)



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

            incision_dist_reps.append(Handle_data.Incision_Dist(incision_data, NSurgeons=8, NControl=8))
            incision_dist_7.append(Handle_data.Incision_Dist_from_7(incision_data, NSurgeons=8, NControl=8))
            incision_dist_1_5.append(Handle_data.Incision_Dist_from_1_5(incision_data, NSurgeons=8, NControl=8))
            rings_dist_reps.append(Handle_data.Rings_Dist(rings_data, NSurgeons=8, NControl=8))
            suture_dist_reps.append(Handle_data.Suture_Dist(suture_data, NSurgeons=7, NControl=8))

        # Uncomment to have first subject only
        # break


# Create Pandas dataframe for the rings peaks

names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]

peaks_dataframe = pd.DataFrame(columns=['Subject', 'Surgeon', 'Age',  'Repetition', 'Peak score'])
index = 0
for i, (subject, is_surgeon, age) in enumerate(zip(names, surgeons, ages)):
    for rep in range(5):
        peaks_dataframe.loc[index] = [subject, is_surgeon, age, rep, len(total_peaks[index])]
        index += 1


# Save data to excel file
file_name = f'Data\Peaks.xlsx'
peaks_dataframe.to_excel(file_name)

# Create Pandas dataframe for the metrics

results_dict = {'incision_dist_reps': incision_dist_reps,
                'suture_dist_reps': suture_dist_reps,
                'rings_dist_reps': rings_dist_reps,
                'incision_dist_7': incision_dist_7,
                'incision_dist_1_5': incision_dist_1_5}

testList = ['incision_dist_reps','suture_dist_reps', 'rings_dist_reps', 'incision_dist_7', 'incision_dist_1_5']

if compute_metrics==True:
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

        print("\n\nSurgeons vs Control for: ", testName, " scored ", pointbiserialr(df2['Surgeon'], df2['Score']) )

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
            #plt.show()
            fig.savefig(f'Images\cross_corr_matrix_{testName}.png')

        # Save data to excel file
        file_name = f'Data\{testName}.xlsx'
        df2.to_excel(file_name)







