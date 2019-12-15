# TODO: Calculate the densities of the cells present in frame #552-554
#  of slice movie (pos0, '17_07_24', 'MDCK_90WT_10Sc_NoComp') manually

import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt
from Local_Cell_Density_Project.SegClass_HDF_Output_Files.HDF_Format_New.HDF5_Data_Functions import GetXandYcoordsPerFrameSLOW
from Local_Cell_Density_Project.SegClass_HDF_Output_Files.HDF_Format_Old.Explore_HDF5_File_Functions import GetXandYcoordinatesPerFrame

# Initiate coordinates of all cells per frame:
hdf5_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/HDF/segmented.hdf5"
print ("Processing the hdf5 file: {}".format(hdf5_file))
x_gfp, y_gfp, x_rfp, y_rfp = GetXandYcoordsPerFrameSLOW(hdf5_file=hdf5_file, frame=1103)
print ("Done with the hdf5 file: {}".format(hdf5_file))


print (x_gfp)
print (y_gfp)
print (x_rfp)
print (y_rfp)

x_coords = x_gfp + x_rfp
y_coords = y_gfp + y_rfp
cells = []

for x, y in zip(x_coords, y_coords):
    if x > 597.0 and x < 598.0 and y > 730.0 and y < 732.0:
        print ("HERE", x, y)


if len(x_coords) == len(y_coords):
    for x, y in zip(x_coords, y_coords):
        cells.append([x, y])
else:
    raise ValueError("Length of 'x-coords' and 'y-coords' vectors are not identical.")

cells = tuple(cells)
print (cells)
areas = [0 for _ in range(len(cells))]
print (areas)


# Now calculate their densities - unit test:
points = np.array(cells)
tri = sp.Delaunay(points)
fig = sp.delaunay_plot_2d(tri=tri)
plt.title("Unit Test - Local Density Analysis\n'MDCK_90WT_10Sc_NoComp', '17_07_24', 'pos0', slice #552")
plt.show()

print (tri.points)
print ("Uno")
print (tri.simplices)
print ("Dos")
print (points[tri.simplices])
print ("Tres")

triangles_all = points[tri.simplices]
print ("Total # of triangles: {}".format(len(triangles_all)))

for number, triangle in enumerate(triangles_all):

    a_x = triangle[0][0]
    a_y = triangle[0][1]
    b_x = triangle[1][0]
    b_y = triangle[1][1]
    c_x = triangle[2][0]
    c_y = triangle[2][1]

    a_edge = np.sqrt( (b_x - c_x) ** 2 + (b_y - c_y) ** 2 )
    b_edge = np.sqrt( (a_x - c_x) ** 2 + (a_y - c_y) ** 2 )
    c_edge = np.sqrt( (a_x - b_x) ** 2 + (a_y - b_y) ** 2 )

    s = (a_edge + b_edge + c_edge) / 2
    area = np.sqrt(s*(s-a_edge)*(s-b_edge)*(s-c_edge))

    print("Triangle #{} = {}\tEdges = {}\tArea = {} pixels^2".format(number + 1, triangle, [a_edge, b_edge, c_edge], area))

    for point in triangle:
        index_x = x_coords.index(point[0])
        index_y = y_coords.index(point[1])
        if index_x == index_y:
            areas[index_x] += 1/area
    #break


print (cells)
print (areas)

for cell, area in zip(cells, areas):
    #if cell[0] > 597.0 and cell[0] < 598.0 and cell[1] > 730.0 and cell[1] < 732.0:
    print (cell, area)