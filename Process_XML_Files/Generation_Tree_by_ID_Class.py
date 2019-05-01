#TODO: Create a script which will import Alan's generation tree code - use 'lineage.py' module.

print ("\nImporting 'lineage.py' script...")
from lineage import *

print ("Parsing through 'tracks_type1.xml' file...")
t = LineageTree.from_xml("/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml")



#TODO: Learn how to access the data stored as classes in each Node.

print ("Creating the lineage tree...\n")
trees = t.create()      # it's a list of Nodes (=classes)
print ("How many nodes in first layer? {}\n".format(len(trees)))

# Individual functions (e.g tree.leaf) are not callable (e.g not tree.leaf())!
# types = e.g. bool, list, int, ... Dictionary is callable! TODO: Why?

def GetCellDetails(cell_ID):
    # --- Call a specific cell via raw_input method:
    #cell_ID = input("Type in cell ID (integer): ".format(0, len(trees)))

    print("\nCell #{} has following parameters:".format(cell_ID))
    FOUND = False
    cells_node = None
    generation = 0

    for order, tree in enumerate(trees):
        # Check if the cell is one of the 'root' cells, i.e if it was directly seeded into the plate:
        if tree.ID == cell_ID:
            FOUND = True
            cells_node = order
            isRoot = True
            print ("\tisRoot -> {} \n\tisLeaf -> {} \n\thasChildren -> {}: {} & {}"\
                        "\n\tappearsFirst -> frame #{} \n\tappearsLast -> frame #{}"\
                        "\n\tmovieTime -> {} mins = {} hrs \n\tdictionary -> {}"\
                   .format(isRoot, tree.leaf, len(tree.children) > 0, tree.children, tree.children,
                        tree.start, tree.end,
                        ((tree.end-tree.start)*4), round((((tree.end-tree.start)*4)/60), 2), tree.to_dict()))
            break
        if len(tree.children) > 0:
            left = tree.children[0]
            right = tree.children[1]


        # Raise a note that the for-loop is done and found (or still haven't found) the cell:
        if order == len(trees) - 1:
            print ("\nFor loop is at the end. Nothing left to iterate over.")
            print ("Found your cell #{}? {}".format(cell_ID, FOUND))
            print ("Which node is cell #{} in? Node #{}".format(cell_ID, cells_node))


GetCellDetails(103)
#GetCellDetails(7158)
