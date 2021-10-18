# Surgery simulation on SOFA Framework
Prototypes of 4 visuo-haptic simulations for surgical training:
  - a suture training task with one device
  - a suture training task with two devices
  - an incision training task
  - a dexterity task
The simulations are developed in the SOFA Framework environment and require the use of a Geomagic Touch Device.

# Main folders


## 1_Medical tasks
Scripts for the prototypes of multiple haptic training surgery tasks to be performed on the SOFA Framework Open Source Software and the Geomagic Touch haptic device. The tasks are Incision_task.py, Rings_task.py, Suture_task.py, Suture_task_double_forceps. The main models for these tasks are in incision_models.py (for incision) and suture_models.py (rings and single/double suture).
The mesh folder contains the mesh data for the models. 

## 2_GUIs
Scripts for three simple GUIs that ease the usability of the simulations, allowing to choose the type of task, the number of haptic devices, etc. (To be completed)

## 2_3D models to print
CAD files to be printed and replaced as Geomagic Touch handle.

## 4_Experiments

### SOFA Scripts
Scripts for the single device tasks for both right-handed and left-handed users. The bats folder contains two main bats to run the correct files in order,  for both right-handed and left-handed users. The SUTURE_ONLY bat files are there in case the main batch files crash after the first suture. The ohter files are simple GUIs that describe the experiment, and are run togehter with the simulations.
### Analyze data
Scripts to analyze data after the experiments: create plots, compute various metrics,..

# Installation and running procedure
## Requirements 
### Software requirements for SOFA scripts
- Sofa v20.12.02 (compiled with sources with the additional Geomagic and SofaPython3 plugins)
### Software requirements for Data analysis and GUIs:
- Conda environment (I used MiniConda3) with: Python 3.9.0, Matplotlib, numpy, pandas, pillow, tkinter, Scipy, Seaborn, Openpyxl. (Note: SOFA requires Python 3.7, while I decided to use Python 3.9 for the 
### Hardware requirements:
- One Geomagic Touch haptic device for all tasks / Two Geomagic Touch devices for the double-device suture.
## Installation
### SOFA simulations
- Install SOFA Framework by following my tutorial or SOFA's tutorial. 
- Copy the Medical simulations folder inside sofa/src.
### GUIs and data analysis
- Create a Miniconda environment with Python 3.9.0
## Running procedure
- Use the GUI that you find inside the GUIs folder to test the simualtions. You can also test a simulation by opening the Command Prompt, typing cd path/to/runsofa then runsofa path/to/task/task.py, by sustituing the name of the python script with the one that you want to run.
- 
# System's limitations
TODO

# Author and contacts
Chiara Saporetti: chiara.saporetti@gmail.com




