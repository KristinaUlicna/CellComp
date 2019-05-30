import matplotlib.pyplot as plt
import os
import sys
sys.path.append("../")

from Cell_Cycle_Duration.Plot_CC_Duration_Hist import PlotHistGenerationCCT
from Sequitr_Lineage_Trees.lineage import LineageTreeNode, LineageTree, LineageTreePlotter


def AnalyseLeftOutliers(txt_file):
    """ Plot lineage trees using Alan's LineageTreePlotter class (from Sequitr github)
        to visualise the whole lineage tree of the cells skewed to the left,
        i.e. appearing between 2 and 1 standard deviations minus the mean
        on the normally distributed histogram for both generations (1 and 2).
        TODO: Extend to 3 generations when data becomes available!
    """

    # First, make sure that you get the specific mean & st.dev for each generation for this specific file:
    call = PlotHistGenerationCCT(txt_file=txt_file)
    call.CreateGenerationList()
    call.PlotHistSimple()
    mean_list = call.mean
    std_list = call.std

    # TODO: This is only done for generation #1!!! Is this correct? Compare to mean & st.dev. of generation 2!
    # Define boundaries of the outliers: upper = 1 st.dev down from mean, lower = 2 st.devs down from mean!
    outlier_boundary_lower = round(mean_list[0] - 2 * std_list[0], 2)
    outlier_boundary_upper = round(mean_list[0] - 1 * std_list[0], 2)

    print ("Outlier boundary lower: {}".format(outlier_boundary_lower))
    print ("Outlier boundary upper: {}".format(outlier_boundary_upper))

    # Find the cells which have doubling time below the mean-std boundary but are not artefacts:

    outliers_list = []
    for line in open(txt_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID":
            continue
        if float(line[4]) > outlier_boundary_lower and float(line[4]) <= outlier_boundary_upper:
            print (line)
            outliers_list.append(int(line[0]))
    print ("\nOutliers List: {}".format(outliers_list))


    # QUESTION: How is the tree iterated over and lines written into the '_raw.txt.' file?
    # ANSWER: FROM THE BACK! If you continue iterating downwards, you get to the root of the tree.

    """
    3445	551	    551	    0	    0.0	    2	False	True
    3446	551	    555	    16	    0.27	2	False	True
    1802	323	    550	    908	    15.13	1	False	False
    8713	958	    1103	580	    9.67	4	False	True
    8710	958	    1083	500	    8.33	4	False	True
    5197	712	    957	    980	    16.33	3	False	False
    5198	712	    1010	1192	19.87	3	False	True
    3158	522	    711	    756	    12.6	2	False	False
    3146	521	    521	    0	    0.0	    2	False	True
    1804	323	    520	    788	    13.13	1	False	False
    1408	270	    322	    208	    3.47	0	True	False
    
    """


    def FindRootofTree(outlier_cellID):
        """ Finds the root of the tree so that you can plot the tree easily.

        Args:
            outlier_cellID (integer)    ->    the cell whose root you want to find

        Return:
            outlier_rootID (integer)    ->    the root to plot lineage tree.

        """

        # Find the parents of these cells - now use '_raw.txt' in REVERSED order:
        raw_file = txt_file.replace("filtered", "raw")
        finding = False         # 'finding' is a marker => from this moment, look for 0 (so it doesn't return first 0 in file)
        for line in open(raw_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or len(line) < 8:
                continue
            if int(line[0]) == outlier_cellID:
                finding = True
            if finding is True and int(line[5]) == 0:
                return int(line[0])


    # Call the function to create the whole list for the roots of the outliers:

    outliers_root = []
    for outlier in outliers_list:
        root = FindRootofTree(outlier)
        outliers_root.append(root)

    print ("\nOutliers Root: {}".format(outliers_root))


    # Plot the lineage trees for all cells identified:

    def PlotLineageTree(root_ID, cell_ID, show=False):
        xml_file = txt_file.replace("/analysis/cellIDdetails_filtered.txt", "/tracks/tracks_type1.xml")
        t = LineageTree.from_xml(xml_file)
        trees = t.create()
        plotter = LineageTreePlotter()

        plt.figure()
        for tree in trees:
            if tree.ID == root_ID:
                plotter.plot([tree])
                plt.title("LinTree_Root_{}_CellID_{}.jpeg".format(root_ID, cell_ID))

        # Save, show & close:
        directory = "/".join(txt_file.split("/")[:-1]) + "/outliers/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        plt.savefig(directory + "LinTree_Root_{}_CellID_{}.jpeg".format(root_ID, cell_ID), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    # Call the function to iterate through the lists of the same length (if not, Exception) to plot trees:
    if len(outliers_list) != len(outliers_root):
        raise Exception("Warning, not all roots have been identified - lists differ in length!")

    for cell_ID, root_ID in zip(outliers_list, outliers_root):
        PlotLineageTree(root_ID=root_ID, cell_ID=cell_ID, show=True)



#AnalyseLeftOutliers("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos6/cellIDdetails_filtered.txt")

#AnalyseLeftOutliers("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos7/cellIDdetails_filtered.txt")

#AnalyseLeftOutliers("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos8/cellIDdetails_filtered.txt")

