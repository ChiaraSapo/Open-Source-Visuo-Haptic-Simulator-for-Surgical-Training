import pandas as pd 
import matplotlib.pyplot as plt

# Read data from txt
# Skip the first 2 rows since they're useless
# Do not use the first column as indices
# Use both tabs and white spaces as separators
# Give specific names to the columns
data = pd.read_csv("SutureNeedle_pos_x.txt",  skiprows=[0,1], index_col=False, delim_whitespace=True, 
names=['Time', 'x1', 'y1', 'z1'])#, 'x2', 'y2', 'z2', 'x3', 'y3', 'z3','x4','y4','z4'])

# Plot data: example
fig=plt.figure()
ax=fig.add_subplot(projection='3d')
ax.scatter(data['x1'],data['y1'],data['z1'])
plt.show()
