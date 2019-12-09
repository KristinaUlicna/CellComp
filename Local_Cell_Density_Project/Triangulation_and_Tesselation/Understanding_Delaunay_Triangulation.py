import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt

# TODO: Find out how to calculate the distances (edges) of the triangles of a single simple triangle:

points = [[0, 0], [4, 0], [0, 3], [4, 6]]
points = np.array(points)
tri = sp.Delaunay(points)
fig = sp.delaunay_plot_2d(tri=tri)
plt.show()

print (tri.points)
print ("Uno")
print (tri.simplices)
print ("Dos")
print (points[tri.simplices])
print ("Tres")

triangles_all = points[tri.simplices]

for triangle in triangles_all:
    a_x = triangle[0][0]
    a_y = triangle[0][1]
    b_x = triangle[1][0]
    b_y = triangle[1][1]
    c_x = triangle[2][0]
    c_y = triangle[2][1]

    a_edge = np.sqrt( (b_x - c_x) ** 2 + (b_y - c_y) ** 2 )
    b_edge = np.sqrt( (a_x - c_x) ** 2 + (a_y - c_y) ** 2 )
    c_edge = np.sqrt( (a_x - b_x) ** 2 + (a_y - b_y) ** 2 )
    print (a_edge, b_edge, c_edge)

    s = (a_edge + b_edge + c_edge) / 2
    area = np.sqrt(s*(s-a_edge)*(s-b_edge)*(s-c_edge))
    print (area)

