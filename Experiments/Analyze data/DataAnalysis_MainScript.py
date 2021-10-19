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
from scipy.spatial import distance
import Suture_Time 
from matplotlib.pyplot import cm
from scipy.stats import spearmanr

subjects_path='.'

## Choose what to compute/plot:
# Plot graphs of incision, rings and suture
plot_incision=False#True
plot_rings=False#True
plot_suture=False#True
# Compute metrics: path length, peaks, mean distance....
compute_metrics=True
create_dataframes=False

# Data for the metrics
incision_dist_reps=[]
incision_min_dist_7=[]
incision_min_dist_1_5=[]
incision_max_dist_7=[]
incision_max_dist_1_5=[]
suture_dist_reps=[]
rings_dist_reps_2D=[]
rings_dist_reps_3D=[]
total_peaks=[]
traj_in_boxes = []
suture_time=[]
suture_peaks = []
rings_peaks = []
incision_peaks = []
NControl = 0
NSurgeons = 0

suture_PL12=[]




################### Count subjects ########################
# Look for all folders and files in specified subjects path
for folder in os.listdir(subjects_path):

    # If "folder" is actually a folder
    if os.path.isdir(subjects_path + '\\' + folder) and not 'Images' in folder and not 'chache' in folder and not 'Data' in folder:# and not 'u7' in folder: # U7 da problemi

        if 's' in folder or 'S' in folder:
            NSurgeons +=1
        if 'u' in folder:
            NControl += 1

Ntot=NSurgeons+NControl
print("COUNT SUBJECTS ENDED: Surgeons: ", NSurgeons, " Control: ", NControl)
#################################################################################################
#################################################################################################
#################################################################################################





################### Retrieve subjects data ########################

person=0

for folder in os.listdir(subjects_path):

    # If "folder" is actually a folder
    if os.path.isdir(subjects_path + '\\' + folder) and not 'Images' in folder and not '__' in folder and not 'Data' in folder:# and not 'u7' in folder: # U7 da problemi

        incision_data = []
        rings_data = []
        rings_data_filtered = []
        suture_data = []
        #incision_peaks = []
        rings_peaks = []

        path =  subjects_path + f'\\{folder}'

        # print(folder)

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
                t = df['Time'].values

                # Save "good" points, i.e. the ones in the skin range
                good = np.where((x <= 9) & (x >= 5) & (y <= 22) & (y >= 11) & (z <= 3) & (z >= -2))[0]

                # Set the min y coordinate as the minimum of the y(t) in the good area
                last = good[np.argmin(y[good])]
                if folder=='u7':
                    good = np.where((x <= 9) & (x >= 5) & (y <= 22) & (y >= 11) & (z <= 3) & (z >= -3))[0]
                #     if 'Rep1' in filename:
                #         last=np.where((t>=20) & (y<=11))[0]
                    if 'Rep2' in filename:
                        good[0]=np.where(t>=15)[0][0]
                        last=np.where((t>18) & (y<=11))[0][0]

                # Save values from the first time the user was in the right position over the skin for the first time,
                # to the last point as defined before
                df_filtered = df.loc[good[0]: last, :]

                # Smooth the height to count peacks better
                #df_filtered['z1'] = df_filtered['z1'].rolling(100).mean()

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

                # if filename=='Rep4_S0_Incision3Pos_Double_x':
                #     y=y[100:]

                # Save "good" points, i.e. the ones in the skin range
                good = np.where((x <= 21) & (x >= 0) & (y <= 17) & (y >= 0) & (z <= 15) & (z >= -0.5))[0]
                first= np.where( (y<=17.5) & (y>14.5) & (x<=15) & (x>=11.5))[0]
                idx = np.where( (y<=5.4) & (y>2.5) & (x<=8) & (x>=5))[0]

                if idx.size!=0:
                    last=idx[0]
                else:
                    last=good[np.argmin(y[good])]
                if first.size==0:
                    first=good
                #print(filename)
                if  filename=='Rep9_u2_RingsPos_Double_x.txt':
                    #print("u222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
                    first= np.where( (y<=16) & (y>14.5) & (x<=15) & (x>=11.5))[0]
                    
                    # i = 2
                    # while int(y[-i]) <= int(y[-i + 1]):  # Possibly add patience
                    #     i += 1
                    # last = len(y) - i

                # Save values from the first time the user was in the right position over the skin for the first time,
                # to the last point as defined before

                df_filtered = df.loc[first[0]: last, :]

                # Smooth the height to count peacks better
                # df_filtered['z1'] = df_filtered['z1'].rolling(50).mean() # UNCOMMENT TO PLOT

                # Save all these modified values are rings data to plot
                rings_data.append(df_filtered)







                df2 = pd.read_csv(path + '\\' + filename, skiprows=[0, 1], engine='python', index_col=False,
                                 delim_whitespace=True,
                                 names=['Time', 'x1', 'y1', 'z1'])

                # Save x,y,z data
                x = df2['x1'].values
                y = df2['y1'].values
                z = df2['z1'].values

                # Save "good" points, i.e. the ones in the skin range
                good = np.where((x <= 21) & (x >= 0) & (y <= 17) & (y >= 0) & (z <= 15) & (z >= -0.5))[0]
                first= np.where( (y<=17.5) & (y>14.5) & (x<=15) & (x>=11.5))[0]
                idx = np.where( (y<=5.4) & (y>2.5) & (x<=8) & (x>=5))[0]

                if idx.size!=0:
                    last=idx[0]
                else:
                    last=good[np.argmin(y[good])]
                if first.size==0:
                    first=good
                if  filename=='Rep11_u2_RingsPos_Double_x':
                    print("u222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
                    first[0]=first[-1]
                
                # Save values from the first time the user was in the right position over the skin for the first time,
                # to the last point as defined before
                df_filtered2 = df2.loc[first[0]: last, :]

                df_filtered2['z1'] = df_filtered2['z1'].rolling(50).mean() # UNCOMMENT TO PLOT: era 50 con prom=1

                # Find indices of the peaks in the height
                p = find_peaks(-df_filtered2['z1'], prominence=1) # Minus to find neg peaks, prominence singe centers are at z=4

                # Desired peaks
                p2 = []

                for peak in p[0]:
                    if df_filtered2['z1'].values[peak] <=2.3: # Take only the ones that touch the skin (?)
                        p2.append(peak)

                # Find the corrensponding time instant of the peaks
                rings_peaks.append(df_filtered2['Time'].values[p2])

                ### NEW 
                real_peaks=[]
                for counter in range(1,len(p2)):
                    elementi=p2[counter]
                    elementii=p2[counter-1]
                    xi=[df_filtered2['x1'].values[elementi], df_filtered2['y1'].values[elementi], df_filtered2['z1'].values[elementi]]
                    xii=[df_filtered2['x1'].values[elementii], df_filtered2['y1'].values[elementii], df_filtered2['z1'].values[elementii]]
                    if distance.euclidean(xi,xii)>1:
                        real_peaks.append(elementi)

                # Data for metrics
                total_peaks.append(real_peaks)
                rings_data_filtered.append(df_filtered2)

                # df_filtered_peaks = df.loc[good[0]: min(last, good[-1]), :]
                # df_filtered_peaks['z1'] = df_filtered_peaks['z1'].rolling(50).mean() # UNCOMMENT TO PLOT

                # # Find indices of the peaks in the height
                # p = find_peaks(-df_filtered_peaks['z1'], prominence=1) # Minus to find neg peaks, prominence singe centers are at z=4

                # # Desired peaks
                # p2 = []

                # for peak in p[0]:
                #     if df_filtered_peaks['z1'].values[peak] <=2.5: # Take only the ones that touch the skin (?)
                #         p2.append(peak)

                # # Find the corrensponding time instant of the peaks
                # rings_peaks.append(df_filtered_peaks['Time'].values[p2])

                # # Data for metrics
                # total_peaks.append(p2)


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
                    first = np.where((x <= 17) & (x >= 10) & (y <= 13) & (y >= 7) & (z <= 15) & (z >= -0.5))[0]
                    idx = np.where( (y<=5.5) & (y>=1) & (x>=5) & (x<=11))[0]

                    if idx.size!=0:
                        last=idx[-1]
                    else:
                        i = 2
                        while int(y[-i]) <= int(y[-i + 1]):  # Possibly add patience
                            i += 1
                        last = len(y) - i


                    # Save values from the first time the user cut the skin for the first time, or at least touched it in the right position
                    df_filtered = df.loc[first[0]: min(last, good[-1]), :]

                    # Smooth the height to count peacks better
                    #df_filtered['z1'] = df_filtered['z1'].rolling(50).mean()

                    # Save all these modified values are suture data to plot
                    suture_data.append(df_filtered)

                    # Find indices of the peaks in the height (Removed for now)
                    p = find_peaks(-df_filtered['z1'], prominence=1) # Minus to find neg peaks, prominence singe centers are at z=4

                    # Desired peaks
                    boxes_x=[8,8,13.5,13.5]
                    boxes_y=[3,10,6,14]
                    boxSize=2

                    person+=1


        suture_PL12.append(Handle_data.Handle_Suture(suture_data, folder))
        # ################### Plot trajectory and height ########################

        if plot_incision==True:
            Handle_data.Incision_Height(incision_data, incision_peaks, filename=folder)
            plt.close('all')
            Handle_data.Incision_Trajectory(incision_data, folder)
            plt.close('all')

        if plot_rings==True:
            Handle_data.Rings_Height(rings_data, rings_peaks, filename=folder)
            plt.close('all')
            Handle_data.Rings_Trajectory(rings_data, filename=folder)
            plt.close('all')

        if plot_suture==True:
            #Handle_data.Suture_Height(suture_data, filename=folder)
            plt.close('all')
            #Handle_data.Suture_Trajectory(suture_data, filename=folder)
            plt.close('all')

        ################### Compute metrics data (except suture time) ########################

        if compute_metrics==True:
            # Save values for pandas dataframes
            if 'S0' not in folder:# and 'u0' not in folder: # Remove this line in future tests
                #traj_in_boxes.append(Handle_data.Suture_Path_Length_per_user_wrt_peaks(suture_data))
                suture_dist_reps.append(Handle_data.Suture_Path_Length_per_user(suture_data))
            incision_dist_reps.append(Handle_data.Incision_Path_Length_per_user(incision_data)) # List of *users* rows and *repetitions* columns
            incision_min_dist_7.append(Handle_data.Incision_Min_Dist_7(incision_data))
            incision_min_dist_1_5.append(Handle_data.Incision_Min_Dist_1_5(incision_data))
            #incision_max_dist_7.append(Handle_data.Incision_Max_Dist_7(incision_data))
            #incision_max_dist_1_5.append(Handle_data.Incision_Max_Dist_1_5(incision_data))
            rings_dist_reps_2D.append(Handle_data.Rings_Path_Length_per_user_2D(rings_data))
            rings_dist_reps_3D.append(Handle_data.Rings_Path_Length_per_user_3D(rings_data))

        # Uncomment to have first subject only
        # break



#print(suture_PL12)
Handle_data.SutPL12(suture_PL12)
# # TODo
# #Handle_data.Mean_Std_Dev_Sut_peaks(suture_peaks)
# print("RETRIEVE AND PLOT SUBJECTS DATA ENDED")

# #print(rings_peaks)
# rings_peaks=[]
# temp_rings_peaks=[]
# for i in range(len(total_peaks)):
#     temp_rings_peaks.append(len(total_peaks[i]))
# splits = np.array_split(temp_rings_peaks, 16)
# for i in range(16):
#     rings_peaks.append(splits[i])



# Handle_data.Incision_barplot(incision_dist_reps, 'Incision 3D Mean Path Length [cm]')
# Handle_data.Incision_barplot(incision_min_dist_1_5,'Incision Mean maximum deviation along z [cm]')
# Handle_data.Incision_barplot(incision_min_dist_7,'Incision Mean maximum deviation along x [cm]')
# plt.close('all')

Handle_data.Metrics_wrt_age(suture_dist_reps, 'Suture', 'Suture 3D Path Length [cm]')
#Handle_data.Metrics_wrt_age(incision_dist_reps, 'Incision', 'Incision 3D Path Length [cm]')
Handle_data.Metrics_wrt_age(incision_min_dist_1_5, 'Incision','Incision Mean maximum deviation along z [cm]')
Handle_data.Metrics_wrt_age(incision_min_dist_7, 'Incision','Incision Mean maximum deviation along x [cm]')
Handle_data.Metrics_wrt_age(rings_dist_reps_3D, 'Rings', 'Rings 3D Path Length [cm]')
Handle_data.Metrics_wrt_age(rings_dist_reps_2D, 'Rings', 'Rings 2D Path Length [cm]')
# plt.close('all')


Handle_data.Metrics_Per_User_Scatter(suture_dist_reps, 'Suture', "Suture 3D Path Length [cm]")
#Handle_data.Metrics_Per_User_Scatter(incision_dist_reps, 'Incision', "Incision 3D Path Length [cm]")
Handle_data.Metrics_Per_User_Scatter(rings_dist_reps_3D, 'Rings', "Rings 3D Path Length [cm]")
Handle_data.Metrics_Per_User_Scatter(rings_dist_reps_2D, 'Rings', "Rings 2D Path Length [cm]")
Handle_data.Metrics_Per_User_Scatter(incision_min_dist_1_5,'Incision','Incision maximum deviation along z [cm]')
Handle_data.Metrics_Per_User_Scatter(incision_min_dist_7,'Incision','Incision maximum deviation along x [cm]')
plt.close('all')


# # Handle_data.Metrics_Mean_Std_Err_Reps(incision_dist_reps,'Incision','Incision Mean Path Length [cm]')
# # Handle_data.Metrics_Mean_Std_Err_Reps(incision_min_dist_1_5,'Incision','Incision Mean maximum deviation along z [cm]')
# # Handle_data.Metrics_Mean_Std_Err_Reps(incision_min_dist_7,'Incision','Incision Mean maximum deviation along x [cm]')
# Handle_data.Metrics_Mean_Std_Err_Reps(rings_dist_reps_2D,'Rings','Rings Mean Path Length 2D [cm]')
# Handle_data.Metrics_Mean_Std_Err_Reps(rings_dist_reps_3D,'Rings','Rings Mean Path Length 3D [cm]')
# #Handle_data.Mean_Std_Dev_All(rings_peaks,'Rings','Peaks number', ' ')
# Handle_data.Metrics_Mean_Std_Err_Reps(suture_dist_reps,'Suture','Suture Mean Path Length 3D [cm]')
# plt.close('all')


# # Handle_data.Metrics_Mean_Std_Err_Barplot_Reps(incision_dist_reps,'Incision','Incision Mean Path Length [cm]')
# # Handle_data.Metrics_Mean_Std_Err_Barplot_Reps(incision_min_dist_1_5,'Incision','Incision Mean maximum deviation along z [cm]')
# # Handle_data.Metrics_Mean_Std_Err_Barplot_Reps(incision_min_dist_7,'Incision','Incision Mean maximum deviation along x [cm]')
# Handle_data.Metrics_Mean_Std_Err_Barplot_Reps(rings_dist_reps_2D,'Rings','Rings Mean Path Length 2D [cm]')
# Handle_data.Metrics_Mean_Std_Err_Barplot_Reps(rings_dist_reps_3D,'Rings','Rings Mean Path Length 3D [cm]')
# #Handle_data.Mean_Std_Dev_All(rings_peaks,'Rings','Peaks number', ' ')
# Handle_data.Metrics_Mean_Std_Err_Barplot_Reps(suture_dist_reps,'Suture','Suture Mean Path Length 3D [cm]')
# plt.close('all')



# Compute 'ideal' values of path length

# if compute_metrics==True:

#     a=[7,22,0]
#     b=[7,11,0]
#     dist=[]
#     dist.append( distance.euclidean( a,b )) #math.sqrt( (x_list1[i]-x_list1[i-1])**2 + (y_list1[i]-y_list1[i-1])**2 + (z_list1[i]-z_list1[i-1])**2) ) 
#     tot_dist=dist
#     print("Incision ideal path length: ", float(np.array(tot_dist)))

#     a=[10,20,0]
#     b=[12,15,0]
#     c=[6,12,0]
#     d=[12,7,0]
#     e=[6,5,0]
#     dist=[]
#     dist.append( distance.euclidean( a,b )) #math.sqrt( (x_list1[i]-x_list1[i-1])**2 + (y_list1[i]-y_list1[i-1])**2 + (z_list1[i]-z_list1[i-1])**2) ) 
#     dist.append( distance.euclidean( b,c ))
#     dist.append( distance.euclidean( c,d ))
#     dist.append( distance.euclidean( d,e ))
#     rings_tot_dist=sum(dist)
#     print("Rings ideal path length: ", rings_tot_dist)

#     a=[10,17,0]
#     b=[15,10,10]
#     c=[7,10,-4]
#     d=[15,5,10]
#     e=[7,3,-4]
#     dist=[]
#     dist.append( distance.euclidean( a,b )) #math.sqrt( (x_list1[i]-x_list1[i-1])**2 + (y_list1[i]-y_list1[i-1])**2 + (z_list1[i]-z_list1[i-1])**2) ) 
#     dist.append( distance.euclidean( b,c ))
#     dist.append( distance.euclidean( c,d ))
#     dist.append( distance.euclidean( d,e ))
#     sut_tot_dist=sum(dist)
#     print("Suture ideal path length: ", sut_tot_dist)



#     print("Incision path: [", min(min(incision_dist_reps)), ", ", max(max(incision_dist_reps)), "]" )#with mean: ", incision_dist_reps.mean())
#     print("Rings path: [", min(min(rings_dist_reps_2D)), ", ", max(max(rings_dist_reps_2D)), "]")
#     print("Suture path: [", min(min(suture_dist_reps)), ", ", max(max(suture_dist_reps)), "]")

# print("'IDEAL' AND REAL VALUES COMPARED")
# #################################################################################################
# #################################################################################################
# #################################################################################################











# # ################### Compute suture time ########################
# # suture_time=Suture_Time.suture_time_computation()
# # plt.close('all')
# # print("COMPUTE SUTURE TIME ENDED")
# # #################################################################################################
# # #################################################################################################
# # #################################################################################################









# Handle_data.Rings_Peaks_Per_User(rings_peaks)
# ################### Create Pandas dataframes for the metrics and save them also as excel files ########################


# print(suture_PL12)
# print(suture_PL12[1])
# print(suture_PL12[1][0])
# print(suture_PL12[1][0][7])
# print(suture_PL12[1][1][7])
suture_PL12=suture_PL12[1:]
# print(len(suture_PL12))




if create_dataframes==True:

    names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [ 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]

    df_suture = pd.DataFrame(columns=['Subject', 'Surgeon', 'Age', 'Repetition', 
                                    'Path Length 1', 'Path Length 2'])

    index = 0

    for i, (subject, is_surgeon, age) in enumerate(zip(names, surgeons, ages)):
            for rep in range(8):
                # if subject=='u0':
                #     df_suture.loc[index] = [subject, is_surgeon, age, float(rep+1), suture_dist_reps[i][rep], -1] # do not consider u0 time
                # if 'u' in subject and not subject=='u0':
                #     df_suture.loc[index] = [subject, is_surgeon, age, float(rep+1), suture_dist_reps[i][rep], suture_time[i-1][rep]]
                # elif 's' in subject:
                #     df_suture.loc[index] = [subject, is_surgeon, age, float(rep+1), suture_dist_reps[i][rep], suture_time[i][rep]]
                df_suture.loc[index] = [subject, is_surgeon, age, float(rep+1), suture_PL12[i][0][rep], suture_PL12[i][1][rep]] 
                index += 1
    #df_suture['Test'] = df_suture['Test'].factorize()[0]

    print(df_suture)
    file_name = f'Data\Metrics - Excel Tables\Suture.xlsx'
    df_suture.to_excel(file_name)
    corr_matrix = df_suture.corr(method='spearman')
    #print(corr_matrix)

    # print("Spearman correlation in suture, pl3d vs group:", spearmanr(df_suture['Surgeon'].values, df_suture['Path Length'].values))
    # print("Spearman correlation in suture, pl3d vs rep:", spearmanr(df_suture['Repetition'].values, df_suture['Path Length'].values))
    # print("Spearman correlation in suture, pl3d vs age:", spearmanr(df_suture['Age'].values, df_suture['Path Length'].values))
    with sns.axes_style("white"):
        corr_matrix = df_suture.corr(method='spearman')
        print(corr_matrix)
        #corr_matrix.drop(['Path Length'], axis=0, inplace=True)

        fig = plt.figure(figsize=(5, 8))
        plt.title('Cross correlations')
        ax = sns.heatmap(
            corr_matrix,#[['Path Length']],
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
        #plt.show()
        fig.savefig(f'Suture.png')





    names = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",    "u0", "u1", "u2", "u3", "u4", "u5", "u6", "u7"]
    surgeons = [1., 1., 1., 1., 1., 1., 1., 1.,   0., 0., 0., 0., 0., 0., 0., 0.]
    ages = [49., 67., 80., 32., 34., 42., 30., 34.,   38., 44., 63., 34., 44., 32., 73., 25]

    df_incision = pd.DataFrame(columns=['Subject', 'Surgeon', 'Age',  'Repetition', 
                                        'Path Length', 'Max Deviation along x','Max Deviation along z (depth)'])

    index = 0
    for i, (subject, is_surgeon, age) in enumerate(zip(names, surgeons, ages)):
        for rep in range(6):
                df_incision.loc[index] = [subject, is_surgeon, age, float(rep+1), incision_dist_reps[i][rep], 
                incision_min_dist_7[i][rep], incision_min_dist_1_5[i][rep]]
                index += 1
    #df_incision['Test'] = df_incision['Test'].factorize()[0]

    #print(df_incision)
    file_name = f'Data\Metrics - Excel Tables\Incision.xlsx'
    df_incision.to_excel(file_name)

    # corr_matrix = df_incision.corr(method='spearman')
    # print(corr_matrix)
    print("Spearman correlation in incision, pl3d vs group:", spearmanr(df_incision['Surgeon'].values, df_incision['Path Length'].values))
    print("Spearman correlation in incision, pl3d vs rep:", spearmanr(df_incision['Repetition'].values[0:48], df_incision['Path Length'].values[0:48]))
    print("Spearman correlation in incision, pl3d vs rep:", spearmanr(df_incision['Repetition'].values[48:], df_incision['Path Length'].values[48:]))
    print("Spearman correlation in incision, pl3d vs age:", spearmanr(df_incision['Age'].values, df_incision['Path Length'].values))
    print("Spearman correlation in incision, max dev x vs group:", spearmanr(df_incision['Surgeon'].values, df_incision['Max Deviation along x'].values))
    print("Spearman correlation in incision, max dev x vs rep:", spearmanr(df_incision['Repetition'].values, df_incision['Max Deviation along x'].values))
    print("Spearman correlation in incision, pmax dev x vs age:", spearmanr(df_incision['Age'].values, df_incision['Max Deviation along x'].values))
    print("Spearman correlation in incision, max dev z vs group:", spearmanr(df_incision['Surgeon'].values, df_incision['Max Deviation along z (depth)'].values))
    print("Spearman correlation in incision, max dev z vs rep:", spearmanr(df_incision['Repetition'].values, df_incision['Max Deviation along z (depth)'].values))
    print("Spearman correlation in incision, max dev z vs age:", spearmanr(df_incision['Age'].values, df_incision['Max Deviation along z (depth)'].values))

    with sns.axes_style("white"):
        corr_matrix = df_incision.corr(method='spearman')
        print(corr_matrix)
        #corr_matrix.drop(['Path Length'], axis=0, inplace=True)

        fig = plt.figure(figsize=(5, 8))
        plt.title('Cross correlation')
        ax = sns.heatmap(
            corr_matrix,#[['Path Length']],
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

        #plt.show()
        fig.savefig(f'Incision.png')




    df_rings = pd.DataFrame(columns=['Subject', 'Surgeon', 'Age', 'Repetition', 'Path Length 2D', 'Path Length 3D'])#, 'Peaks Number'])

    index = 0
    peak_index=0
    for i, (subject, is_surgeon, age) in enumerate(zip(names, surgeons, ages)):
        for rep in range(6):
            df_rings.loc[index] = [subject, is_surgeon, age, rep+1, rings_dist_reps_2D[i][rep], rings_dist_reps_3D[i][rep] ]#  , rings_peaks[i][rep]]
            index += 1
            peak_index+=1
    #df_rings['Test'] = df_rings['Test'].factorize()[0]
    stupidachiara=df_rings['Path Length 2D'].values
    indexs=61
    df_rings['Path Length 2D'].values[indexs]=40.6807094971098
    indexs2=65
    df_rings['Path Length 2D'].values[indexs2]=58.988452639756
    stupidachiara=df_rings['Path Length 3D'].values
    #indexs=np.where(stupidachiara==45.188295957607)[0]
    df_rings['Path Length 3D'].values[indexs]=48.456240049782
    #indexs2=np.where(stupidachiara==47.7605225257734)[0]
    df_rings['Path Length 3D'].values[indexs2]=66.7650444532981
    #print(df_rings)
    file_name = f'Data\Metrics - Excel Tables\Rings.xlsx'
    df_rings.to_excel(file_name)
    with sns.axes_style("white"):
        corr_matrix = df_rings.corr(method='spearman')
        print(corr_matrix)
        #corr_matrix.drop(['Path Length'], axis=0, inplace=True)

        fig = plt.figure(figsize=(5, 8))
        plt.title('Cross correlation')
        ax = sns.heatmap(
            corr_matrix,#[['Path Length']],
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
        #plt.show()
        fig.savefig(f'Rings.png')



    # corr_matrix = df_rings.corr(method='spearman')
    # print(corr_matrix)

    # print("Spearman correlation in rings, pl3d vs group:", spearmanr(df_rings['Surgeon'].values, df_rings['Path Length 3D'].values))
    # print("Spearman correlation in rings, pl3d vs rep:", spearmanr(df_rings['Repetition'].values, df_rings['Path Length 3D'].values))
    # print("Spearman correlation in rings, pl3d vs age:", spearmanr(df_rings['Age'].values, df_rings['Path Length 3D'].values))
    # print("Spearman correlation in rings, pl2d vs group:", spearmanr(df_rings['Surgeon'].values, df_rings['Path Length 2D'].values))
    # print("Spearman correlation in rings, pl2d vs rep:", spearmanr(df_rings['Repetition'].values, df_rings['Path Length 2D'].values))
    # print("Spearman correlation in rings, pl2d vs age:", spearmanr(df_rings['Age'].values, df_rings['Path Length 2D'].values))
    # print("Spearman correlation in rings, peaks vs group:", spearmanr(df_rings['Surgeon'].values, df_rings['Peaks Number'].values))
    # print("Spearman correlation in rings, peaks vs rep:", spearmanr(df_rings['Repetition'].values, df_rings['Peaks Number'].values))
    # print("Spearman correlation in rings, peaks vs age:", spearmanr(df_rings['Age'].values, df_rings['Peaks Number'].values))


    print("CREATION PANDAS DATAFRAMES ENDED")
#################################################################################################
#################################################################################################
#################################################################################################


plt.close('all')
#################################################################################################
#################################################################################################
#################################################################################################


























