# Create a directory to try different tracker config models. Copy /HDF/segmented.hdf5 into each of those paths.

import shutil
import os

def HDFtoFolder(config_number):
    source_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/HDF/segmented.hdf5"

    new_directory = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
                        "tracker_performance_evaluation/tracks_try_{}/HDF/".format(config_number)
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    result = shutil.copy(src=source_file, dst=new_directory)
    print ("HDF folder, containing 'segmented.hdf5' file copied into config try {};\n\t{}".format(config_number, result))


def CopyLineageTreeToFolder(config_number, tree_root_ID=1):
    old_dir = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
               "tracks_try_{}/analysis/channel_RFP/trees/".format(int(config_number))
    if os.path.exists(old_dir):
        new_dir = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
                  "tracker_performance_evaluation/example_tree_comparison/"
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        old_file = "LinTree_Root_{}.png".format(int(tree_root_ID))
        if os.path.isfile(old_dir + old_file):
            new_file = "LinTree_Root_{}_Config_{}.png".format(int(tree_root_ID), int(config_number))

            result = shutil.copy(src=old_dir + old_file, dst=new_dir + new_file)
            print("Tree with root #{} from config #{} was copied into designated folder."
              .format(int(tree_root_ID), int(config_number)))
        else:
            print("The file with tree with root #{} does not exist. "
                  "Check if tracking & subsequent analysis of config #{} ran correctly..."
                  .format(int(tree_root_ID), int(config_number)))
    else:
        print ("The folder with tree with root #{} does not exist. "
               "Check if tracking & subsequent analysis of config #{} ran correctly..."
               .format(int(tree_root_ID), int(config_number)))


def MakeAllConfigAnalysisIdentical(config_number):
    # First, create a 'tracks' folder in the 'tracks_try_XX' folder:
    old_dir = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
                "tracker_performance_evaluation/tracks_try_{}/".format(config_number)
    new_dir_tracks = old_dir + "tracks/"
    if not os.path.exists(new_dir_tracks):
        os.makedirs(new_dir_tracks)

    # Now move each file from the old directory into the newly created directory:
    for file in os.listdir(old_dir):
        shutil.move(src=old_dir + file, dst=new_dir_tracks)


def DeleteAnalysisFolder(config_number):
    dir = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
          "tracker_performance_evaluation/analysis_try_{}/".format(config_number)

    shutil.rmtree(path=dir, ignore_errors=True)


#Call the funciton:
for i in range(1, 50):
    CopyLineageTreeToFolder(config_number=i, tree_root_ID=20)