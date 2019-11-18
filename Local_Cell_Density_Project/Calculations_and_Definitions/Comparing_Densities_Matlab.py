# TODO: Read the cell density superfile ('.mat') which combines the matrices for all 18 'MDCK_WT_Pure' movies:

# TODO: Header =   [cell_ID,
#                   cell_type (0=GFP, 1=RFP),
#                   total no. of neighbours,
#                   total number of SIMILAR neighbours,
#                   total number of DIFFERENT neighbours,
#                   frame,
#                   average area (mean distance)
#                   cell density (Voronoi Tesselation]

import numpy as np
import scipy.io
import matplotlib.pyplot as plt

file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/tracks/density_nhood.mat"
mat = scipy.io.loadmat(file_name=file)      # it's a dictionary!


# Loop through the file to create dictionaries for each date & pos:

for key, value in mat.items():
    if 'density' in str(key) and isinstance(value, np.ndarray):
        value = value.tolist()
        data = value[0][0][0]
        #print (data)
        print (len(data))
        counter = 0
        for mini_list in data:
            if int(mini_list[0]) == 60:
                if int(mini_list[1]) == 1:
                    print (mini_list)
                    counter += 1
        print (counter)
        # Extract all relevant information into a channel-specific dictionary (GFP & RFP IDs would otherwise clash!)
        dict_GFP = {}
        dict_RFP = {}

        index = 0
        while index < len(data):
            cell_ID = int(data[index][0])
            cell_type = int(data[index][1])
            frame = int(data[index][5])
            density = float(data[index][7])

            if cell_type == 0:
                if cell_ID not in dict_GFP:
                    dict_GFP[cell_ID] = []
                dict_GFP[cell_ID].append([frame, density])

            elif cell_type == 1:
                if cell_ID not in dict_RFP:
                    dict_RFP[cell_ID] = []
                dict_RFP[cell_ID].append([frame, density])
            else:
                raise Exception("Error: Cell type of cell ID {} not defined. "
                                "Cell type = {} (should be 0 = GFP or 1 = RFP)".format(cell_ID, cell_type))
            index += 1

        # TODO: Now iterate over the dictionaries to extract information about cells in a file-writable format:
        # Header = [Cell_ID, ...]

        #print ("\nDictionary: {}".format(dictionary))
        """
        for k, v in dict_GFP.items():
            if k == 23:
                print (k, v)
                print (len(v))
                for mini_list in v:
                    plt.scatter(mini_list[0], mini_list[1], color="dodgerblue")

        for k, v in dict_RFP.items():
            if k == 23:
                print(k, v)
                print(len(v))
                for mini_list in v:
                    plt.scatter(mini_list[0], mini_list[1], color="green")

        plt.ylim(0, 0.0005)
        plt.show()
        plt.close()
        """
        #print ("\nDictionary GFP: {}".format(dict_GFP))
        #print ("\nDictionary RFP: {}".format(dict_RFP))

        """
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
        """

