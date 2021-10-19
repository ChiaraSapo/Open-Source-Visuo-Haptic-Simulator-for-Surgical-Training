# Surgery simulation on SOFA Framework
Prototypes of 4 visuo-haptic simulations for surgical training:
  - a suture training task with one device
  - a suture training task with two devices
  - an incision training task
  - a dexterity task
The simulations are developed in the SOFA Framework environment and require the use of a Geomagic Touch Device.

# Main folders


## 1_Medical tasks
Scripts for the prototypes of multiple haptic training surgery tasks to be performed on the SOFA Framework Open Source Software and the Geomagic Touch haptic device. The tasks scripts are two (for right-handed and left-handed subjects):
- Incision_task_Right.py, Incision_task_Left.py
- Rings_task.py, Rings_task_Left.py
- Suture_task.py, Suture_task_Left.py
- Suture_task_double_forceps, Suture_task_double_forceps_Left.py

The main models for these tasks are in incision_models.py (for incision) and suture_models.py (rings and single/double suture).

The mesh folder contains the mesh data for the models. 

## 2_GUIs
Scripts for GUIs that ease the usability of the simulations, allowing to choose the type of task, the number of haptic devices, and the dominant hand. At this moment only a single-type station (one device) is allowed, so the double-device suture cannot be run. If the user chooses a double-device station, the single-device one will still be run.

## 2_3D models to print
CAD files of the handles to be printed and replaced on the Geomagic Touch.

## 4_Experiments

### SOFA Scripts
This folder contains the files I used for the experiments: the Bats folder contains the two main batch files that run the tests: BAT_Right.bat and BAT_Left.bat (for right-handed and left-handed users). The python files are scripts for GUIs to be run during the experiment.

To use these files modify the bat files variables: CONDAPATH, ENVNAME, SIMULPATH by setting the paths on your computer

### Analyze data
Scripts to analyze data after the experiments: create plots, compute various metrics, ...



# Installation and running procedure
## Requirements 
### Software requirements for SOFA scripts
- Sofa v20.12.02 (compiled with sources with the additional Geomagic and SofaPython3 plugins)
### Software requirements for Data analysis and GUIs:
- Conda environment (I used MiniConda3) with: Python 3.9.0, Matplotlib, numpy, pandas, pillow, tkinter, Scipy, Seaborn, Openpyxl. (Note: SOFA requires Python 3.7, while I decided to use Python 3.9 for the other scripts)
### Hardware requirements:
- One Geomagic Touch haptic device for all tasks / Two Geomagic Touch devices for the double-device suture.

## Installation
### SOFA simulations
- Copy the MedicalSimulations folder inside sofa/src.

### GUIs 
- Copy the GUIs folder to a desired location. 
- In GUIs/Config.txt file substitute the first line with your/path/to/runsofa
- In GUIs/Config.txt file substitute the second line with your/path/to/MedicalSimulations
- In GUIs/FIRST_TIME.bat and GUIs/EVERY_TIME.bat modify the variables: CONDAPATH, ENVNAME by setting the paths on your computer

### Data analysis tools (for full experimental session data only)
- Copy the Analyze Data folder to a desired location.
- In DataAnalysis_MainScript.py 
  - plot_incision, plot_rings, plot_suture variables to true if you want to plot the single subjects results (results are saved into Images folder). 
  - compute metrics to plot the single subject and all subejcts metrics (results are saved into Data\Metrics - Single User folder).
  - create_dataframes to save the pandas dataframes with information on all tasks and also export them in excel files (results are saved into Data\Metrics - Excel Tables).
  
## Running procedure
Use  GUIs/FIRST_TIME.bat to set the environment variables the first time. Then use GUIs/EVERY_TIME.bat to test the simultions. 

Note:You can also test a simulation by opening the Command Prompt, typing cd path/to/runsofa then runsofa path/to/task/task.py, by sustituting the name of the python script with the one that you want to run.


# System's limitations
TODO

# Author and contacts
Chiara Saporetti: chiara.saporetti@gmail.com




