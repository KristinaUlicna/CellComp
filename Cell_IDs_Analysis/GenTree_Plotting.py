# ----- LineageTree Plotting -----

#TODO: Plot one tree at a time.

import sys
sys.path.append("../")
import matplotlib.pyplot as plt
from Sequitr_Lineage_Trees.lineage import LineageTreeNode, LineageTree, LineageTreePlotter

t = LineageTree.from_xml("/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_type2.xml")
trees = t.create()

plotter = LineageTreePlotter()

plt.figure()
for tree in trees:
    plotter.plot([tree])
    plt.show()
    plt.close()