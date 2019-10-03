# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
# ----- Job Script Creator for SegClass & Tracking Jobs ----- #
#                                                             #
# ----- Creator :           Kristina ULICNA             ----- #
#                                                             #
# ----- Last updated :      13th May 2019               ----- #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import sys
sys.path.append("../")

# Call the class 'ProcessMovies' & its 'SegClass' & 'Tracking' functions:

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths
from JobScript_Creator.JobScriptCreator_Class import ProcessMovies


# Iterate through all movies available in selected folder:

#xml_file_list, _ = GetMovieFilesPaths(exp_type="MDCK_90WT_10Sc_NoComp")

"""
for file in sorted(xml_file_list):
    if "tracks_type1" in file:
        if "17_07_24" in file and "pos13" in file:
            continue
        print("Writing job for file: {}".format(file))
        #ProcessMovies(xml_file=file).SegClass(BF=True, GFP=True, RFP=True)
        ProcessMovies(xml_file=file).Tracking(to_track_GFP=True, to_track_RFP=True)
"""


"""
dir_exp_type = "/Volumes/lowegrp/Data/Kristina/MDCK_Sc_Tet+_Pure/"
server_dir = os.listdir(dir_exp_type)
for folder in server_dir:
    if folder != ".DS_Store":
        dir_data_date = dir_exp_type + folder + "/"
        print (dir_data_date)
        folders_pos = os.listdir(dir_data_date)
        for pos in folders_pos:
            if pos != ".DS_Store":
                dir_pos = dir_data_date + pos + "/"
                print (dir_pos)
                folders_tracks = os.listdir(dir_pos)
                for tracks_folder in folders_tracks:
                    if tracks_folder == "tracks":
                        dir_tracks = dir_pos + "tracks/"
                        print (dir_tracks)
                        dir_xml = os.listdir(dir_tracks)
                        for file in dir_xml:
                            if file == "tracks_type1.xml":
                                xml_file = dir_tracks + file
                                print (xml_file)
                                ProcessMovies(xml_file=xml_file).SegClass(BF=True, GFP=False, RFP=True)
"""


# Loop through multiple positions:
"""
for position in range(0, 9):
    call = ProcessMovies(position, data_date='17_07_31')
    #call.SegClass()
    call.Tracking()

for position in range(6, 9):
    call = ProcessMovies(position, data_date='17_07_24')
    #call.SegClass()
    call.Tracking()

for position in [0, 1, 2, 11, 12, 13]:
    call = ProcessMovies(position, data_date='17_07_10')
    #call.SegClass()
    call.Tracking()

for position in range(7, 10):
    call = ProcessMovies(position, data_date='17_01_24')
    call.SegClass()
    call.Tracking()
"""


# Create jobs for a single, specific position:
"""
call = ProcessMovies(pos=0, data_date='17_03_27', exp_type="MDCK_90WT_10Sc_NoComp", user="Kristina")
call.Tracking(to_track_GFP=True, to_track_RFP=True)

call = ProcessMovies(pos=4, data_date='17_03_27', exp_type="MDCK_90WT_10Sc_NoComp", user="Kristina")
call.Tracking(to_track_GFP=True, to_track_RFP=True)
"""

# Track your template movie:
call_template = ProcessMovies(pos=13, data_date='17_07_24', exp_type="MDCK_90WT_10Sc_NoComp", user="Kristina")
call_template.Tracking(to_track_GFP=False, to_track_RFP=True, try_number=13_2)


# Segment HeLa from Cell Tracking Challenge Dataset:

#call_1 = ProcessMovies(pos=1, data_date='HeLa_H2B_GFP_GT', exp_type="Cell_Tracking_Challenge", user="Kristina")
#call_1.SegClass(BF=False, GFP=True, RFP=False)
#call_1.Tracking(to_track_GFP=True, to_track_RFP=True)

#call_2 = ProcessMovies(pos=2, data_date='HeLa_H2B_GFP_GT', exp_type="Cell_Tracking_Challenge", user="Kristina")
#call_2.SegClass(BF=False, GFP=True, RFP=False)
#call_2.Tracking(to_track_GFP=True, to_track_RFP=True)

