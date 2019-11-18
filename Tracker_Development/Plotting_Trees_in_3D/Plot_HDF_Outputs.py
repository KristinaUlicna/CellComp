#TODO: Plot the scatter plot of all cells in 3D

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Local_Cell_Density_Project.SegClass_HDF_Output_Files.HDF_Format_Old.Explore_HDF5_File_Functions import GetXandYcoordinatesPerFrame


file = '/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/HDF/segmented.hdf5'

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for frame in range(0, 1105):
    x_gfp, y_gfp, x_rfp, y_rfp = GetXandYcoordinatesPerFrame(hdf5_file=file, frame=frame)
    ax.scatter(x_gfp, y_gfp, frame)
    ax.scatter()


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin


n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
