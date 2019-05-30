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
from JobScriptCreator_Class import ProcessMovies


# Iterate through all movies available in selected folder:
# 'MDCK_WT_Pure' or 'MDCK_Sc_Tet-_Pure' or 'MDCK_Sc_Tet+_Pure'


xml_file_list, _ = GetMovieFilesPaths(exp_type="MDCK_90WT_10Sc_NoComp")

for file in xml_file_list:
    if "pos0" in file:
        print("Writing job for file: {}".format(file))
        ProcessMovies(xml_file=file).Tracking(to_track_GFP=True, to_track_RFP=True)



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
call = ProcessMovies(6, data_date='17_07_24')
call.SegClass()
call.Tracking()
"""