#TODO: Create a script to extract first and last frame of cells for which you plotted lin. trees:

import os
import json

dir_json_files = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_RFP/"
dir_lin_tree = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/reconstruct_trees/"

cell_ID_list = []
for cell_ID in os.listdir(dir_lin_tree):
    cell_ID = cell_ID.split("Root_")[-1].split(".jpeg")[0]
    cell_ID_list.append(int(cell_ID))

for cell_ID in sorted(cell_ID_list):
    with open(dir_json_files + "track_{}_RFP.json".format(cell_ID)) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            if key == "t":
                print (cell_ID, "\t\t\t", int(value[0]), int(value[-1]))

