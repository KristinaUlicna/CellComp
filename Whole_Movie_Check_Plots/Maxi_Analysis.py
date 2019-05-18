# TODO: Do the analysis of all server movies at the same time:

import sys
sys.path.append("../")

from Server_Movies_Paths import GetMovieFilesPaths
from Cell_IDs_Analysis.Extractor_CellIDdetails_Class import GetCellDetails
from Whole_Movie_Check_Plots.Sort_CellIDs_Numerically import SortCellIDFile
from Whole_Movie_Check_Plots.Filter_Root_Leaf_CellIDs import FilterRootLeafCellIDs
from Whole_Movie_Check_Plots.Tracking_Plots_Class import AnalyseAllCellIDs

import time
start_time = time.process_time()


# Iterate through all movies:
xml_file_list, txt_file_list = GetMovieFilesPaths()


# Extract cell_ID details by iterating trees:
"""
for xml_file in xml_file_list:
    print ("Processing XML file: {}".format(xml_file))
    GetCellDetails(xml_file=xml_file).IterateTrees()
    print("XML file processed in {} seconds".format(round(time.process_time() - start_time, 2)))
"""

# Sort the cell_IDs in numerical order:
"""
for txt_file in txt_file_list:
    print ("Processing TXT file: {}".format(txt_file))
    SortCellIDFile(txt_file=txt_file)
    print("XML file processed in {} seconds".format(round(time.process_time() - start_time, 2)))
"""

# Filter for files to be used for cell cycle duration analysis:
"""
for sorted_file in txt_file_list:
    sorted_file = sorted_file.replace("raw", "sorted")
    print ("Sorted file (input): {}".format(sorted_file))
    FilterRootLeafCellIDs(txt_file=sorted_file)
    print("Sorted file processed in {} seconds".format(round(time.process_time() - start_time, 2)))
"""

# Do the sanity check for all the movies:

for sorted_file in txt_file_list:
    sorted_file = sorted_file.replace("raw", "sorted")
    print ("Sorted file (input): {}".format(sorted_file))
    call = AnalyseAllCellIDs(txt_file=sorted_file)
    call.PlotCellIDLifeTime()
    call.PlotCellIDsPerFrame()
    call.PlotCellCycleAbsoluteTime()
    for i in [80, 40, 20, 5, 2]:
        call.PlotHist_CellCycleDuration(limit=i)
    print("Sorted file processed in {} seconds".format(round(time.process_time() - start_time, 2)))
