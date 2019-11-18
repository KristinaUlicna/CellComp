# TASK: Exploring the new structure of the HDF file after the September update.
#
# The structure is: ['coords', 'labels', 'map'] where:
#       'coords' = [t (frame), x, y, z, type (1=GFP, 2=RFP)]
#       'labels' = [_, _, _, _, _, _] -> probability of an object is in inter-, prometa-, meta-, anaphase or apoptosis
#       'map' = [0, X] for frame #0 -> cumulative cell count (or rather 'segmented object count') per each frame.
#               last number of previous frame is starting number of following frame, [0, 95], [95, 193], [193, 286],...

import h5py
import matplotlib.pyplot as plt

filename = '/Volumes/lowegrp/Data/Kristina/Cells_FUCCI_Silvia/P00003_mCherry_HDF/segmented.hdf5'
f = h5py.File(filename, 'r')

print ("Hdf5 file keys:\t\t{}".format(list(f.keys())))       # to list the individual keys
print ("Hdf5 file values:\t{}".format(list(f.values())))     # summary, e.g number of members (here, 1105)...
print ("List of members:\t{}".format(list(f['objects'])))     # list of how the 1105 members are called

# Access data in ['frames_0']
print ("Keys per frame:\t{}".format(list(f["objects"]["obj_type_1"].keys())))
print ("Values per frame:\t{}".format(list(f["objects"]["obj_type_1"].values())))

# Access data in ['coords', 'labels', 'map']:
print ("'Coords' per frame:\t{}".format(f["objects"]["obj_type_1"]["coords"]))                  # len = 216 (both GFP & RFP)
print ("'Coords' per frame:\t{}".format(list(f["objects"]["obj_type_1"]["coords"][0:10])))      # [t (frame), x, y, z, type (1=GFP, 2=RFP)]

print ("'Map' per frame:\t{}".format(f["objects"]["obj_type_1"]["map"]))
print ("'Map' per frame:\t{}".format(list(f["objects"]["obj_type_1"]["map"][0:10])))
