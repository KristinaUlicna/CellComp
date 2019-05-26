# ----- LineageTree Plotting -----

#TODO: Plot one tree at a time.

import sys
sys.path.append("../")
import matplotlib.pyplot as plt
from Sequitr_Lineage_Trees.lineage import LineageTreeNode, LineageTree, LineageTreePlotter

t = LineageTree.from_xml("/Users/kristinaulicna/Documents/Rotation_2/tracks_type1_17_07_31_pos0.xml")
trees = t.create()

plotter = LineageTreePlotter()

plt.figure()
for order, tree in enumerate(trees):
    print (tree)
    if order <= 5:
        plotter.plot([tree])
plt.show()