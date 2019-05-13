from Analysis_And_Plotting_Class import *
import time
start_time = time.process_time()

# Temporary file:
#call = AnalyseCellIDs("/Users/kristinaulicna/Documents/Rotation_2/cellIDinfo_vertest.txt")
#call.SortCellIDFile()
#call.PlotCellIDLifeTime()
#call.PlotCellIDsPerFrame()
#call.PlotCellCycleAbsoluteTime()
#call.PlotHist_CellCycleDuration(limit=80)
#call.PlotHist_CellCycleDuration(limit=40)
#call.PlotHist_CellCycleDuration(limit=10)
#call.PlotHist_CellCycleDuration(limit=2)

#TODO: Raise exception to run 'SortCellIDFile()' function if the second file line[0] is not cellID = 1!

# All tracker versions at once:

# TODO: Iterate over all available movies on the server:

for version in range(0, 5):
    call = AnalyseCellIDs("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracker_Updates_XML_Files/"
                          "ver{}/cellIDinfo_ver{}.txt".format(str(version), str(version)))
    call.SortCellIDFile()
    call.PlotCellIDLifeTime()
    call.PlotCellIDsPerFrame()
    call.PlotCellCycleAbsoluteTime()
    for i in [80, 40, 20, 2]:
        call.PlotHist_CellCycleDuration(limit=i)

print ("Done! Processing took {} minutes.".format(round((time.process_time() - start_time) / 60, 2)))