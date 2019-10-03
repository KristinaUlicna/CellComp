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

rep_movie = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"
"""
# Do the sanity check for raw txt_file:
print("Plotting movie graphs...")
call = AnalyseAllCellIDs(txt_file=rep_movie)
call.PlotHistCellCycleDuration(show=True)
call.PlotCellIDLifeTime(show=True)
call.PlotCellIDsPerFrame(show=True)
call.PlotCellCycleAbsoluteTime(show=True)
print ("Done 1!")

# Do the sanity check for sorted txt_file:
rep_movie_sort = rep_movie.replace("raw", "sorted")
call = AnalyseAllCellIDs(txt_file=rep_movie_sort)
call.PlotHistCellCycleDuration(show=True)
call.PlotCellIDLifeTime(show=True)
call.PlotCellIDsPerFrame(show=True)
call.PlotCellCycleAbsoluteTime(show=True)
print ("Done 2!")
"""

# Plot stacked histograms for all generations captured per movie:
hist = PlotHistGenerationCCT(txt_file=rep_movie)
hist.CreateGenerationList(print_stats=True)
hist.PlotHistSimple(show=True)
hist.PlotHistNormalised(show=True)
hist.PlotHistCumulative(show=True)

#VisualiseCellIDRelabelling(txt_file=rep_movie, show=True, print_stats=True)

print("Plotting movie graphs done in {} mins".format(round((time.process_time() - start_time) / 60, 2)))
