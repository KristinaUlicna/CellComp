from Analysis_And_Plotting_Class import *
import time
import os
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


# Iterate over all available movies on the server:

dir_exp_type = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/"
server_dir = os.listdir(dir_exp_type)

for folder in server_dir:
    if folder != ".DS_Store":
        dir_data_date = dir_exp_type + folder + "/"
        #print (dir_data_date)
        folders_pos = os.listdir(dir_data_date)
        for pos in folders_pos:
            if pos != ".DS_Store":
                dir_pos = dir_data_date + pos + "/"
                #print (dir_pos)
                folders_tracks = os.listdir(dir_pos)
                for tracks_folder in folders_tracks:
                    if tracks_folder == "tracks":
                        dir_tracks = dir_pos + "tracks/"
                        #print (dir_tracks)
                        dir_analysis = os.listdir(dir_tracks)
                        for analysis in dir_analysis:
                            if analysis == "analysis":
                                analysis_folder = dir_tracks + "analysis/"
                                #print (analysis_folder)
                                dir_cell_ID = os.listdir(analysis_folder)
                                for cell_ID_file in dir_cell_ID:
                                    if cell_ID_file == "cellIDdetails.txt":
                                        call = AnalyseCellIDs(txt_file = analysis_folder + cell_ID_file)
                                        call.SortCellIDFile()
                                        call.PlotCellIDLifeTime()
                                        call.PlotCellIDsPerFrame()
                                        call.PlotCellCycleAbsoluteTime()
                                        for i in [80, 40, 20, 2]:
                                            call.PlotHist_CellCycleDuration(limit=i)
                                        print ("DONE! Cell ID file {}".format(analysis_folder + cell_ID_file))


# Loop through all versions of the xml_file you have in your Mac folder:
"""
for version in range(0, 5):
    call = AnalyseCellIDs("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracker_Updates_XML_Files/"
                          "ver{}/cellIDinfo_ver{}.txt".format(str(version), str(version)))
    call.SortCellIDFile()
    call.PlotCellIDLifeTime()
    call.PlotCellIDsPerFrame()
    call.PlotCellCycleAbsoluteTime()
    for i in [80, 40, 20, 2]:
        call.PlotHist_CellCycleDuration(limit=i)
"""

# Analyse an individual file specified by an absolute directory:
"""
call = AnalyseCellIDs("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos6/tracks/analysis/cellIDdetails.txt")
call.SortCellIDFile()
call.PlotCellIDLifeTime()
call.PlotCellIDsPerFrame()
call.PlotCellCycleAbsoluteTime()
for i in [80, 40, 20, 2]:
    call.PlotHist_CellCycleDuration(limit=i)
"""

print ("Done! Processing took {} minutes.".format(round((time.process_time() - start_time) / 60, 2)))