# ----- LineageTree Plotting -----

#TODO: Plot one tree at a time.
#TODO: Check if my Node#8 tree I translated from the JSON format corresponds.

import matplotlib.pyplot as plt
from lineage import LineageTreeNode, LineageTree, LineageTreePlotter
t = LineageTree.from_xml("/Users/kristinaulicna/Documents/Rotation_2/tracks_type1_ver3.xml")
trees = t.create()
print(trees)

plotter = LineageTreePlotter()

plt.figure()
for order, tree in enumerate(trees):
    if order == 5:
        plotter.plot([tree])
plt.show()