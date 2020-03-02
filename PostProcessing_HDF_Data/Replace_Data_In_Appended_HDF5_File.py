import h5py
import numpy as np

filename = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/HDF_copy/segmented.hdf5"
f = h5py.File(filename, 'a')

density = f["objects"]["obj_type_1"]["density"]
print (list(density[0:100]))
print (type(density))
print (len(density))
print (type(density[0]))
print (len(density[0]))

for line in range(320272):
    print (density[line][1])
    density[line][1] = 1
    print (density[line][1])

print (list(density[0:100]))
print (type(density))
print (len(density))
print (type(density[0]))
print (len(density[0]))

if f.__bool__():
    f.close()

"""
array1 = np.array([2, 2, 2, 0, 2, 0, 2])
array1[1] = 1
print (array1)
"""