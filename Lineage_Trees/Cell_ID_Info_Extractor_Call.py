# # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                 #
# ----- LineageTree : CellID Info Extractor ----- #
#                                                 #
# ----- Creator :       Kristina ULICNA     ----- #
#                                                 #
# ----- Last Updated :  13th May 2019       ----- #
#                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # #

from Cell_ID_Info_Extractor_Class import *
import os

# Call the class for all available movies:

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
                        dir_xml = os.listdir(dir_tracks)
                        for file in dir_xml:
                            if file == "tracks_type1.xml":
                                xml_file = dir_tracks + file
                                #print (xml_file)
                                GetCellDetails(xml_file=xml_file).IterateTrees()
                                print ("XML file {} done!".format(xml_file))

# Call the class:
"""
for version in list(range(0, 5)):
    if txt_file.closed:
        txt_file = open("/Users/kristinaulicna/Documents/Rotation_2/temporary.txt", 'w')
    else:
        GetCellDetails(version=version).IterateTrees()
"""
#TODO: Why can I not iterate over the class calling?


# Call the class separately:
GetCellDetails(version=4).IterateTrees()