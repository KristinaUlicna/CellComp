#TODO: Make a function to choose which cells are left or right outliers:

import sys
sys.path.append("../")

from Cell_Cycle_Duration.Plot_CC_Duration_Hist import PlotHistGenerationCCT


def ShortlistOutliers(left_or_right="left"):
    """
    Args:
        left_or_right (string) -> "left" or "right" or "middle"

    """

    # First, make sure that you get the specific mean & st.dev for each generation for this specific file:
    file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"
    call = PlotHistGenerationCCT(txt_file=file)
    call.CreateGenerationList()
    mean_list = call.mean
    std_list = call.std
    print ("\nGenerational means:\t{}".format(mean_list))
    print ("Generational st.dev:\t{}".format(std_list))

    # TODO: This is only done for generation #1!!! Is this correct? Compare to mean & st.dev. of generation 2!
    # Define boundaries of the outliers: upper = 1 st.dev down from mean, lower = 2 st.devs down from mean!
    if left_or_right == "left":
        outlier_boundary_lower = round(mean_list[0] - 2 * std_list[0], 2)
        outlier_boundary_upper = round(mean_list[0] - 1 * std_list[0], 2)
    if left_or_right == "right":
        outlier_boundary_lower = round(mean_list[0] + 1 * std_list[0], 2)
        outlier_boundary_upper = round(mean_list[0] + 2 * std_list[0], 2)
    if left_or_right == "middle":
        outlier_boundary_lower = round(mean_list[0] - 1 * std_list[0], 2)
        outlier_boundary_upper = round(mean_list[0] + 1 * std_list[0], 2)
    if left_or_right != "left" and left_or_right != "right" and left_or_right != "middle":
        raise Exception("Warning, specify which outliers you want: 'left' or 'right' or 'middle'")
    print ("Outlier boundaries: lower = {}, upper = {}".format(outlier_boundary_lower, outlier_boundary_upper))


    # Find the cells which have doubling time below/above the one or two st.devs far from the mean:

    outliers_list = []
    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date":
            continue
        if float(line[4]) > outlier_boundary_lower and float(line[4]) <= outlier_boundary_upper:
            outliers_list.append(line[0])
    print ("Outliers List: len = {} -> {}".format(len(outliers_list), outliers_list))

    return outliers_list
