# TODO: Read the cell density superfile ('.mat') which combines the matrices for all 18 'MDCK_WT_Pure' movies:

import matplotlib.pyplot as plt
import numpy as np
import scipy.io
file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/MatLabScripts/Neighbourhood_Analysis-master/data_structures_MDCK_WT_Pure.mat"
mat = scipy.io.loadmat(file_name=file)

print (type(mat))       # it's a dictionary!
#print (mat)
print ()

# Universal loop:

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
        print ("\nDictionary: {}".format(dictionary))

        # Write the created date & pos-specific dictionary of all cells into a file:
        directory = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/MatLabScripts/Density_Txt_Files/"
        name = str(key).split("_")[-1]
        density_file = open(directory + name + ".txt", "w")
        density_file.write(str(dictionary))
        density_file.close()
        print ("File processed: {}".format(name))
        # TODO: Save to folder on server where the data comes from! (date, pos)


# Plot an example cell density over time:
# TODO: Read the dictionary from file rather than from this script!

"""
for cellID, data in dictionary.items():
    if cellID == 7264:
        print (data, type(data))
        fig = plt.figure()
        for mini_list in data:
            plt.scatter(mini_list[0], mini_list[1])
            plt.title("Cell ID: {}".format(cellID))
            plt.xlim(1122, 1142)
            plt.ylim(0.001, 0.00115)
        plt.show()
"""