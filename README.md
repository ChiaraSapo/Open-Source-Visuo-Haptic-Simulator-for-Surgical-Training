# Surgery simulation on SOFA Framework
Prototypes of 4 visuo-haptic simulations for surgical training:
  - a suture training task with one device
  - a suture training task with two devices
  - an incision training task
  - a (more generic) dexterity task
The simulations are developed in the SOFA Framework environment and require the use of a Geomagic Touch Device.

# Main folders

## 1_SOFA installation
PDF with instructions to install the Open-Source software

## 2_GUI
Scripts for three simple GUIs that ease the usability of the simulations, allowing to choose the type of task, the number of haptic devices, etc. (To be completed)

## 3_Medical simulations
Scripts for the prototypes of multiple haptic training surgery tasks to be performed on the SOFA Framework Open Source Software and the Geomagic Touch haptic device. The tasks are Incision_task.py, Rings_task.py, Suture_task.py, Suture_task_double_forceps. The main models for these tasks are in incision_models.py (for incision) and suture_models.py (rings and single/double suture).
The mesh folder contains the mesh data for the models. 

## 3D models to print
CAD files to be printed and replaced as Geomagic Touch handle.

## Experiments

### SOFA Scripts
Scripts for the single device tasks for both right-handed and left-handed users. The bats folder contains two main bats to run the correct files in order,  for both right-handed and left-handed users. The SUTURE_ONLY bat files are there in case the main batch files crash after the first suture. The ohter files are simple GUIs that describe the experiment, and are run togehter with the simulations.
### Analyze data
Scripts to analyze data after the experiments: create plots, compute various metrics,..

# Installation and running procedure
## Software requirements
- Sofa v20.12.02 
- Plugins: Geomagic, SofaPython3
- Matplotlib, numpy, pandas, pillow, tkinter.

## Hardware requirements
- Geomagic Touch Device 

# System's limitations
TODO

# Author and contacts
TODO




