# ----- LineageTree Plotting -----

#TODO: Plot one tree at a time.
#TODO: Check if my Node#8 tree I translated from the JSON format corresponds.

from lineage import LineageTreeNode, LineageTree, LineageTreePlotter
t = LineageTree.from_xml("/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml")
trees = t.create()

for tree in trees:
    LineageTreePlotter.plot(tree=tree)
    break