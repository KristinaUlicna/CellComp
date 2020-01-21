import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt

#points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])
points = np.array([[3, 0], [4.2, 1], [0, 8], [1, 5], [1, 1], [1, 2], [3.5, 0], [4, 1], [6, 6]])

vor = sp.Voronoi(points)
print (vor)
tri = sp.Delaunay(points)
print (tri)

fig = sp.voronoi_plot_2d(vor)
fig = sp.delaunay_plot_2d(tri)
plt.show()
plt.close()