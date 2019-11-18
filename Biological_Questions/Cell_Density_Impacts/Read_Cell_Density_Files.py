# TODO: Read the cell density superfile ('.mat') which combines the matrices for all 18 'MDCK_WT_Pure' movies:

import numpy as np
import scipy.io
import os
file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/MatLabScripts/Neighbourhood_Analysis-master/data_structures_MDCK_WT_Pure.mat"
mat = scipy.io.loadmat(file_name=file)      # it's a dictionary!


# Loop through the file to create dictionaries for each date & pos:

for key, value in mat.items():
    if 'density' in str(key) and isinstance(value, np.ndarray):
        dictionary = {}
        value = value.tolist()
        index = 0
        while index < len(value[0][0][0]):
            cellID = int(value[0][0][0][index][0])
            frame = int(value[0][0][0][index][5])
            density = float(value[0][0][0][index][7])
            if cellID not in dictionary:
                dictionary[cellID] = []
            dictionary[cellID].append([frame, density])
            index += 1
        #print ("\nDictionary: {}".format(dictionary))

        # Write the created date & pos-specific dictionary of all cells into a file:
        name = str(key).split("_")[-1]
        date = name[0:2] + "_" + name[2:4] + "_" + name[4:6]
        pos = str(key).split(name[4:6])[-1].split("density")[0]

        directory = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/{}/{}/density/".format(date, pos)
        if not os.path.exists(directory):
            os.makedirs(directory)

        density_file = open(directory + "cellID_density.txt", "w")
        density_file.write(str(dictionary))
        density_file.close()
        print ("File processed: {}".format(name))
