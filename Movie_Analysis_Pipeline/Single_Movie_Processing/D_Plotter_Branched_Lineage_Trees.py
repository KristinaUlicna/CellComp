import matplotlib.pyplot as plt
import os
import sys
sys.path.append("../")

from Tracker_Development.Sequitr_Package_Scripts.lineage_temp_use_for_HDF import LineageTree, LineageTreePlotter


def PlotLineageTree(xml_file, show=False):
    """ Plots the Lineage tree when the root_ID is not a leaf cell as well;
        i.e. when the cell has children and was tracked after division.
        The directory to the xml_file from which cell originated must be given. """

    # Which position & date is the data in?
    # /Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks_try_1/tracks_type2.xml
    directory = xml_file.split("/")[:-1]
    tracks_name, movie_pos, movie_date = directory[-1], directory[-2], directory[-3]
    analysis_name = tracks_name.replace("tracks", "analysis")
    if "tracks_type1.xml" in xml_file:
        channel_name = "GFP"
    if "tracks_type2.xml" in xml_file:
        channel_name = "RFP"

    # Define the directory to save into, show & close:
    directory = "/".join(directory[:-1]) + "/{}/channel_{}/trees/".format(analysis_name, channel_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the trees, & iterate through them to make the plot:
    t = LineageTree.from_xml(xml_file)
    trees = t.create()
    plotter = LineageTreePlotter()

    counter_total = 0
    counter_plotted = 0

    #for tree in trees[:1]:
    for tree in trees:
        counter_total += 1
        if tree.root is True and tree.leaf is False:
            plotter.plot([tree])
            plt.title("LinTree: Root #{}; {}, {}".format(tree.ID, movie_pos, movie_date))
            plt.savefig(directory + "LinTree_Root_{}.png".format(tree.ID), bbox_inches="tight")
            if show is True:
                plt.show()
            plt.close()
            counter_plotted += 1

    return counter_total, counter_plotted


"""
# Try to understand what the LineageTreePlotter does:
xml_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos0/tracks/tracks_type1.xml"
trees = LineageTree.from_xml(filename=xml_file).create()
plotter = LineageTreePlotter().plot(tree=[trees[8]])
"""