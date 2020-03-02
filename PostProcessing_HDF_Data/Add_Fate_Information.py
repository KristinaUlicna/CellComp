# TODO: Add Fate information from the JSON files to the HDF5 file. Do via numerical shortcuts, not using whole words.

import h5py
import json
import numpy as np

from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths


def Extract_Fates_from_JSON(hdf5_file):
    """

    Legend:
    class Fates(enum.Enum):
        FALSE_POSITIVE = 0
        INITIALIZE = 1
        TERMINATE = 2
        LINK = 3
        DIVIDE = 4
        APOPTOSIS = 5
        MERGE = 6
        EXTRUDE = 7
        INITIALIZE_BORDER = 10
        INITIALIZE_FRONT = 11
        TERMINATE_BORDER = 20
        TERMINATE_BACK = 21
        DEAD = 666
        UNDEFINED = 999


    :param hdf5_file:
    :return:
    """

    fates = []
    fates_numerical = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 20, 21, 666, 999]
    fates_worded = ["FALSE_POSITIVE", "INITIALIZE", "TERMINATE", "LINK", "DIVIDE", "APOPTOSIS", "MERGE", "EXTRUDE",
                    "INITIALIZE_BORDER", "INITIALIZE_FRONT", "TERMINATE_BORDER", "TERMINATE_BACK", "DEAD", "UNDEFINED"]

    json_tracks_dir = hdf5_file.replace("/HDF/segmented.hdf5", "/tracks/tracks_GFP/")
    f = h5py.File(hdf5_file, 'r')

    for cell in f["tracks"]["obj_type_1"]["LBEPR"]:

        with open(json_tracks_dir + "track_{}_GFP.json".format(int(cell[0])), 'r') as json_file:
            data = json.load(json_file)

            if data['fate'] in fates_worded:
                fate_number = fates_numerical[fates_worded.index(data['fate'])]
                fates.append(fate_number)

            else:
                raise AttributeError("Warning, the fate {} doesn't even exist...")

    if f.__bool__():
        f.close()

    return fates



def Append_Fates_to_HDF(hdf5_file):
    """

    :param hdf5_file:
    :return:
    """

    fates = Extract_Fates_from_JSON(hdf5_file=hdf5_file)

    f = h5py.File(hdf5_file, 'a')

    if "fates" in list(f["tracks"]["obj_type_1"]):
        del f["tracks"]["obj_type_1"]["fates"]

    grp = f["tracks"]["obj_type_1"]
    grp.create_dataset(name="fates", data=np.array(fates, dtype=np.int32))

    if f.__bool__():
        f.close()


"""
movies = Get_MDCK_Movies_Paths()
for movie in movies:
    if "AB" in movie:
        continue
    if "GV0794" in movie:
        continue
    if "GV0795" in movie:
        continue
    if "GV0796" in movie:
        continue
    hdf5_file = movie + "HDF/segmented.hdf5"
    Append_Fates_to_HDF(hdf5_file=hdf5_file)
    print ("Done for movie: {}".format(movie))
"""

