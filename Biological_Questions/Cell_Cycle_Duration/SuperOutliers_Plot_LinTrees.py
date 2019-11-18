import time
start_time = time.process_time()

import sys
sys.path.append("../")

from Biological_Questions.Cell_Cycle_Duration.Shortlist_Outliers import ShortlistOutliers
from Movie_Analysis_Pipeline.Merging_Movie_Datasets.Find_Family_Class import FindFamily
from Cell_IDs_Analysis.Plotter_Lineage_Trees import PlotLineageTree

file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"

# Identify the stacked histogram outliers:
left_outliers = ShortlistOutliers(left_or_right="left")
print ()
print (len(left_outliers), left_outliers)

left_outliers_cellID_info = []
left_outliers_parent_info = []
left_outliers_rootID_info = []
for outlier in left_outliers:
    outlier_info = FindFamily(cell_ID=outlier, filtered_file=file).FindItself()
    left_outliers_cellID_info.append(outlier_info)
    parent_info = FindFamily(cell_ID=outlier, filtered_file=file).FindParent()
    left_outliers_parent_info.append(parent_info)
    rootID_info = FindFamily(cell_ID=outlier, filtered_file=file).FindRoot()
    left_outliers_rootID_info.append(rootID_info)

print (len(left_outliers_cellID_info), left_outliers_cellID_info)
print (len(left_outliers_parent_info), left_outliers_parent_info)
print (len(left_outliers_rootID_info), left_outliers_rootID_info)


# Identify the outliers of those outliers & plot their trees:

counter = 0
for outlier_str, outlier, parent, root in zip\
            (left_outliers, left_outliers_cellID_info, left_outliers_parent_info, left_outliers_rootID_info):
    if parent[1] != "NaN" and outlier[1] != "NaN":
        if parent[1] - outlier[1] >= 0:
            counter += 1
            movie = outlier_str.split("-")
            cell_ID = movie[0]
            pos = movie[1]
            date = movie[2]
            xml_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/{}/{}/tracks/tracks_type1.xml".format(date, pos)
            PlotLineageTree(root_ID=root[0], cell_ID=cell_ID, xml_file=xml_file, show=True)

print ("{} outliers were identified & their lineage trees plotted in {} mins."
       .format(counter, round((time.process_time() - start_time) / 60, 2)))