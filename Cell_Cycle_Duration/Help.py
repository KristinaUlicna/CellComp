import sys
sys.path.append("../")

"""
from Whole_Movie_Check_Plots.Tracking_Plots_Class import AnalyseAllCellIDs
call = AnalyseAllCellIDs("/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_sorted.txt")
for i in [80, 40, 20, 5, 2]:
    call.PlotHist_CellCycleDuration(limit=i, show=True)
"""

from Cell_Cycle_Duration.Plot_CC_Duration_Hist import PlotHistGenerationCCT
PlotHistGenerationCCT("/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_filtered.txt", show=True)
#PlotHistGenerationCCT("/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_sorted.txt", show=True)
