#TODO: Filter which trees you want to run the PSO test on - cherry-pick into a new folder:

import os
import shutil

dir_old = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_RFP/"
dir_new = dir_old.replace("tracks_RFP", "chosen_trees_PSO")

if not os.path.exists(dir_new):
    os.makedirs(dir_new)

branches = [15, 48, 402, 406, 733, 738, 20, 163, 633, 635, 160, 329, 539,
            541, 869, 881, 659, 1090, 1002, 999, 61, 59, 433, 432, 692, 691]

for branch in branches:
    file = "track_{}_RFP.json".format(branch)
    shutil.copyfile(src=dir_old + file, dst=dir_new + file)

print ("Done!")