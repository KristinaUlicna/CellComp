# Do the analysis of single selected server movie all at once:

import time
start_time = time.process_time()

from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths
from Movie_Analysis_Pipeline.Single_Movie_Processing.A_Extractor_CellIDdetails_Class import GetCellDetails
from Movie_Analysis_Pipeline.Single_Movie_Processing.B_Processor_TxtFile_RawToFiltered import FilterRawTxtFile
from Movie_Analysis_Pipeline.Single_Movie_Processing.C_Checker_General_Movie_Graphs import AnalyseAllCellIDs
from Movie_Analysis_Pipeline.Single_Movie_Processing.D_Plotter_Branched_Lineage_Trees import PlotLineageTree


# Which movies to analyse? Create a list [one-item list if single movie]:
movies = Get_MDCK_Movies_Paths()

for movie in movies:
    print (movie)
    xml_file = movie + "/tracks/tracks_type1.xml"
    print ("Currently reconstructing trees...")
    call_D = PlotLineageTree(xml_file=xml_file)
    print ("Trees_total = {}; Trees_plotted = {}".format(call_D[0], call_D[1]))


#call_C.PlotCellIDRelabelling(print_stats=True)
#TODO: print_stats=True     Fix ZeroDivisionError
#TODO: print_stats=False    ValueError: shape mismatch: objects cannot be broadcast to a single shape
