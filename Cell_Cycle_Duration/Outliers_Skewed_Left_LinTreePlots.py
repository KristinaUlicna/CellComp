import sys
sys.path.append("../")

from Cell_Cycle_Duration.Plot_CC_Duration_Hist import PlotHistGenerationCCT
from Cell_Cycle_Duration.Find_Family_Class import FindFamily
from Cell_IDs_Analysis.Plotter_Lineage_Trees import PlotLineageTree


def AnalyseLeftOutliers(txt_file):
    """ Plot lineage trees using Alan's LineageTreePlotter class (from Sequitr github)
        to visualise the whole lineage tree of the cells skewed to the left,
        i.e. appearing between 2 and 1 standard deviations minus the mean
        on the normally distributed histogram for both generations (1 and 2).
        TODO: Extend to 3 generations when data becomes available!

    Args:
        txt_file (string)   -> filtered or merged? - apparently, filtered...

    """

    # First, make sure that you get the specific mean & st.dev for each generation for this specific file:
    call = PlotHistGenerationCCT(txt_file=txt_file)
    call.CreateGenerationList()
    mean_list = call.mean
    std_list = call.std
    print ("Generational means:\t{}".format(mean_list))
    print ("Generational st.dev:\t{}".format(std_list))

    # TODO: This is only done for generation #1!!! Is this correct? Compare to mean & st.dev. of generation 2!
    # Define boundaries of the outliers: upper = 1 st.dev down from mean, lower = 2 st.devs down from mean!
    outlier_boundary_lower = round(mean_list[0] - 2 * std_list[0], 2)
    outlier_boundary_upper = round(mean_list[0] - 1 * std_list[0], 2)
    print ("Outlier boundaries: lower = {}, upper = {}".format(outlier_boundary_lower, outlier_boundary_upper))


    # Find the cells which have doubling time below the mean-std boundary but are not artefacts:

    outliers_list = []
    for line in open(txt_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID":
            continue
        if float(line[4]) > outlier_boundary_lower and float(line[4]) <= outlier_boundary_upper:
            outliers_list.append(int(line[0]))
    print ("\nOutliers List: {}".format(outliers_list))


    # Call the function to store the respective root cells for the outliers:

    outliers_root = []
    for outlier in outliers_list:
        root_info = FindFamily(cell_ID=outlier, filtered_file=txt_file).FindRoot()
        outliers_root.append(root_info[0])
    print("Outliers Root: {}".format(outliers_root))

    # Check if the lists of the same length:
    if len(outliers_list) != len(outliers_root):
        raise Exception("Warning, not all roots have been identified - lists differ in length!")


    # Plot the lineage trees for all cells identified:

    xml_file = txt_file.replace("/analysis/cellIDdetails_filtered.txt", "/tracks/tracks_type1.xml")
    for cell_ID, root_ID in zip(outliers_list, outliers_root):
        PlotLineageTree(root_ID=root_ID, cell_ID=cell_ID, xml_file=xml_file, show=True)






#AnalyseLeftOutliers("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos6/cellIDdetails_filtered.txt")

#AnalyseLeftOutliers("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos7/cellIDdetails_filtered.txt")

#AnalyseLeftOutliers("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos8/cellIDdetails_filtered.txt")

