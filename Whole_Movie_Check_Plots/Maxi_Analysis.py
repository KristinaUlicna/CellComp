# TODO: Do the analysis of all server movies at the same time:

import sys
sys.path.append("../")

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths
from Cell_IDs_Analysis.Extractor_CellIDdetails_Class import GetCellDetails
from Whole_Movie_Check_Plots.Process_Raw_TxtFile import ProcessRawTxtFile
from Whole_Movie_Check_Plots.Tracking_Plots_Class import AnalyseAllCellIDs
from Whole_Movie_Check_Plots.Tracking_CellID_Relabelling import VisualiseCellIDRelabelling
from Cell_Cycle_Duration.Plot_CC_Duration_Hist import *

import time
start_time = time.process_time()


# Iterate through all movies:
xml_file_list, txt_file_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")


# Extract cell_ID details by traversing trees:
"""
for xml_file in xml_file_list:
    print ("Processing XML file: {}".format(xml_file))
    GetCellDetails(xml_file=xml_file).IterateTrees()
    print("XML file processed in {} seconds".format(round(time.process_time() - start_time, 2)))
"""

# Process Raw TxtFile:
"""
for txt_file in txt_file_list:
    print ("Processing _raw.txt file: {}".format(txt_file))
    call = ProcessRawTxtFile(raw_file=txt_file)
    call.TrimCellIDFile(trimming_limit=75)
    call.SortCellIDFile()
    call.FilterCellIDFile()
    print("File processed in {} seconds".format(round(time.process_time() - start_time, 2)))
"""

# Do the sanity check for all the movies:

for raw_file in txt_file_list:
    print("Plotting movie graphs for file: {}".format(raw_file))
    call = AnalyseAllCellIDs(txt_file=raw_file)
    call.PlotCellIDLifeTime()
    call.PlotCellIDsPerFrame()
    call.PlotCellCycleAbsoluteTime()
    call.PlotHistCellCycleDuration(limit=80)
    VisualiseCellIDRelabelling(raw_file)
    sorted_file = raw_file.replace("raw", "sorted")
    call = AnalyseAllCellIDs(txt_file=sorted_file)
    call.PlotCellIDLifeTime()
    call.PlotCellIDsPerFrame()
    call.PlotCellCycleAbsoluteTime()
    call.PlotHistCellCycleDuration(limit=80)
    print("Plotting movie graphs done in {} mins".format(round((time.process_time() - start_time) / 60, 2)))


# Plot stacked histograms for all generations captured per movie:
"""
for filtered_file in txt_file_list:
    filtered_file = filtered_file.replace("raw", "filtered")
    print("Filtered file (input): {}".format(filtered_file))
    try:
        # Some files are empty so nothing can be plotted - prevent printing an error message:
        PlotHistGenerationCCT(txt_file=filtered_file, show=True)
    except:
        print ("File {} could not be processed!".format(filtered_file))
    print("Plotting generational histogram took {} seconds".format(round(time.process_time() - start_time, 2)))
"""

# Plot stacked histograms for all generations in ALL movies at once:
"""
PlotHistGenerationCCT("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt", show=True)

"""