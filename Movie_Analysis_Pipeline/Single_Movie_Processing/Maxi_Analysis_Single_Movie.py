# Do the analysis of single selected server movie all at once:

import time
start_time = time.process_time()

from Movie_Analysis_Pipeline.Single_Movie_Processing.A_Extractor_CellIDdetails_Class import GetCellDetails
from Movie_Analysis_Pipeline.Single_Movie_Processing.B_Processor_TxtFile_RawToFiltered import FilterRawTxtFile
from Movie_Analysis_Pipeline.Single_Movie_Processing.C_Checker_General_Movie_Graphs import AnalyseAllCellIDs
from Movie_Analysis_Pipeline.Single_Movie_Processing.D_Plotter_Branched_Lineage_Trees import PlotLineageTree


# Which movies to analyse? Create a list [one-item list if single movie]:
for i in [56]:
    xml_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/tracks_try_{}/tracks/tracks_type2.xml".format(i)
    raw_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/tracks_try_{}/analysis/channel_RFP/cellIDdetails_raw.txt".format(i)

    call_A = GetCellDetails(xml_file=xml_file).IterateTrees()
    call_B = FilterRawTxtFile(raw_file=raw_file)
    call_C = AnalyseAllCellIDs(txt_file=raw_file)
    call_C.PlotCellIDLifeTime()
    call_C.PlotCellIDsPerFrame()
    call_C.PlotCellCycleAbsTime()
    call_C.PlotHistCellCycleTime()

    call_D = PlotLineageTree(xml_file=xml_file)
    print ("Trees_total = {}; Trees_plotted = {}".format(call_D[0], call_D[1]))


#call_C.PlotCellIDRelabelling(print_stats=True)
#TODO: print_stats=True     Fix ZeroDivisionError
#TODO: print_stats=False    ValueError: shape mismatch: objects cannot be broadcast to a single shape
