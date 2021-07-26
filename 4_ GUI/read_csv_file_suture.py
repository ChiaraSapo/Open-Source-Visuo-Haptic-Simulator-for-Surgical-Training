import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Read data from txt
# Skip the first 2 rows since they're useless
# Do not use the first column as indices
# Use both tabs and white spaces as separators
# Give specific names to the columns


data = pd.read_csv("C:/sofa/build/v20.12.02/bin/Release/SutureTask_pos_x.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, 
names=['Time', 'x1', 'y1', 'z1'])

print(data)








# Plot data: example
fig=plt.figure()
ax=fig.add_subplot(projection='3d')
ax.plot(data['x1'],data['y1'],data['z1'], label="Trajectory", color="salmon", linewidth="3.5")
ax.set_title("End effector position in space")
ax.set_xlabel('x direction')
ax.set_ylabel('y direction')
ax.set_zlabel('z direction')
ax.grid()
plt.show()





#fig=plt.figure()
fig, ((ax, ax1), (ax2, ax3)) = plt.subplots(2,2)
fig.suptitle('Position, Velocity,  Force')


ax.plot(data['x1'], data['y1'], label="pos_x", color="salmon", linewidth="3.5")
#ax1.set_title("End effector position in time")
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.legend()
ax1.grid()
#ax1.show()

ax1.plot(data['Time'],data['x1'], label="pos_x", color="salmon", linewidth="3.5")
ax1.plot(data['Time'],data['y1'], label="pos_y", color="darkturquoise", linewidth="3.5")
ax1.plot(data['Time'],data['z1'], label="pos_z", color="palegreen", linewidth="3.5")
#ax1.set_title("End effector position in time")
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Positions')
ax1.legend()
ax1.grid()
#ax1.show()


data = pd.read_csv("C:/sofa/build/v20.12.02/bin/Release/SutureTask_vel_v.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, 
names=['Time', 'x1', 'y1', 'z1'])

# Plot data: example
ax2.plot(data['Time'],data['x1'], label="vel_x", color="salmon", linewidth="3.5")
ax2.plot(data['Time'],data['y1'], label="vel_y", color="darkturquoise", linewidth="3.5")
ax2.plot(data['Time'],data['z1'], label="vel_z", color="palegreen", linewidth="3.5")
#ax2.set_title("End effector velocity in time")
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Velocities')
ax2.legend()
ax2.grid()



data = pd.read_csv("C:/sofa/build/v20.12.02/bin/Release/SutureTask_force_f.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, 
names=['Time', 'x1', 'y1', 'z1'])

# Plot data: example
ax3.plot(data['Time'],data['x1'], label="force_x", color="salmon", linewidth="3.5")
ax3.plot(data['Time'],data['y1'], label="force_y", color="darkturquoise", linewidth="3.5")
ax3.plot(data['Time'],data['z1'], label="force_z", color="palegreen", linewidth="3.5")
#ax3.set_title("End effector force in time")
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Forces')
ax3.legend()
ax3.grid()
plt.show()



# fig=plt.figure()
# plt.plot(data['Time'],data['x1'], label="pos_x", color="salmon", linewidth="3.5")
# plt.plot(data['Time'],data['y1'], label="pos_y", color="darkturquoise", linewidth="3.5")
# plt.plot(data['Time'],data['z1'], label="pos_z", color="palegreen", linewidth="3.5")
# plt.title("End effector position in time")
# plt.xlabel('Time [s]')
# plt.ylabel('Positions')
# plt.legend()
# plt.grid()
# plt.show()


# data = pd.read_csv("C:/sofa/build/v20.12.02/bin/Release/SutureNeedle_vel_v.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, 
# names=['Time', 'x1', 'y1', 'z1'])

# # Plot data: example
# fig=plt.figure()
# plt.plot(data['Time'],data['x1'], label="vel_x", color="salmon", linewidth="3.5")
# plt.plot(data['Time'],data['y1'], label="vel_y", color="darkturquoise", linewidth="3.5")
# plt.plot(data['Time'],data['z1'], label="vel_z", color="palegreen", linewidth="3.5")
# plt.title("End effector velocity in time")
# plt.xlabel('Time [s]')
# plt.ylabel('Velocities')
# plt.legend()
# plt.grid()
# plt.show()


# data = pd.read_csv("C:/sofa/build/v20.12.02/bin/Release/SutureNeedle_force_f.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, 
# names=['Time', 'x1', 'y1', 'z1'])

# # Plot data: example
# fig=plt.figure()
# plt.plot(data['Time'],data['x1'], label="force_x", color="salmon", linewidth="3.5")
# plt.plot(data['Time'],data['y1'], label="force_y", color="darkturquoise", linewidth="3.5")
# plt.plot(data['Time'],data['z1'], label="force_z", color="palegreen", linewidth="3.5")
# plt.title("End effector force in time")
# plt.xlabel('Time [s]')
# plt.ylabel('Forces')
# plt.legend()
# plt.grid()
# plt.show()