import sys
sys.path.append("../")

from Cell_Cycle_Duration.Plot_CC_Duration_Hist import PlotHistGenerationCCT

call = PlotHistGenerationCCT("/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_merged.txt")
call.CreateGenerationList(print_stats=True)
call.PlotHistSimple(show=True)
call.PlotHistNormalised(show=True)
call.PlotHistCumulative(show=True)
