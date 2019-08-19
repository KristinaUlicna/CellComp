import matplotlib.pyplot as plt
import os
import sys
sys.path.append("../")

from Sequitr_Lineage_Trees.lineage import LineageTree, LineageTreePlotter


def PlotLineageTree(root_ID, cell_ID, xml_file, show=False):
    """ Plots the Lineage tree when cell_ID (query cell), its root_ID
        & the xml_file from which the cell originated are given. """

    # Which position & date is the data in?
    movie_pos = xml_file.split("/")[-3]
    movie_date = xml_file.split("/")[-4]

    # Create the trees, & iterate through them to make the plot:
    t = LineageTree.from_xml(xml_file)
    trees = t.create()
    plotter = LineageTreePlotter()

    plt.figure()
    for tree in trees:
        if tree.ID == root_ID:
            plotter.plot([tree])
            plt.title("LinTree: Root #{}, CellID #{}, {}, {}".format(root_ID, cell_ID, movie_pos, movie_date))


    # Define the directory to save into, show & close:
    directory = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/reconstruct_trees/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if show is True:
        plt.savefig(directory + "LinTree_Root_{}.jpeg".format(root_ID), bbox_inches="tight")
        plt.show()
        plt.close()
