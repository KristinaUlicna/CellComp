#TODO: Create 'analysis' folder on the server where the 'HDF' and 'tracks' are:

directory = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/hahaha/"

import os
if not os.path.exists(directory):
    os.makedirs(directory)
file = open(directory + "this_file.txt", "w")