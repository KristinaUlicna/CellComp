# TASK: Exploring the new structure of the HDF file after the September update.

"""


                                      'coords'          ... shape (320272, 5) = total number of observations per movie,
                                       |                                      [t (frame), x, y, z, type (1=GFP, 2=RFP)]
                     'obj_type_1'------o---- 'map'      ... shape (320272, 6) = total number of observations per movie,
                       |          |    |                                      [_, _, _, _, _, _] -> softmax probability
                       |          |   'labels'          ... shape (1105, 2) = length of the movie
          'objects'----o          |                                           [_, _] -> starting & finishing cell count
            |          |           --TODO-- 'density' & 'nhood'
            |          |
            |        'obj_type_2'----- ... ditto
            |
            |
    f ----- o
            |                         'dummies' -> list of non-assigned dummy objects while tracking
            |                          |
            |        'obj_type_1'------o---- 'map' -> by length in descending order; indexing the respective coords will give whole track information
            |          |               |
            |          |              'tracks' -> ordered indeces of how tracks go in the 'coords' object maxi-list
          'tracks'-----o
                       |
                       |
                     'obj_type_2'----- ... ditto

"""
#
#
#
#
#
#
#
# The structure is: ['coords', 'labels', 'map'] where:
#       'coords' = [t (frame), x, y, z, type (1=GFP, 2=RFP)]
#       'labels' = [_, _, _, _, _, _] -> probability of an object is in inter-, prometa-, meta-, anaphase or apoptosis
#       'map' = [0, X] for frame #0 -> cumulative cell count (or rather 'segmented object count') per each frame.
#               last number of previous frame is starting number of following frame, [0, 95], [95, 193], [193, 286],...

import h5py
import matplotlib.pyplot as plt


filename = '/Users/kristinaulicna/Documents/Rotation_2/Example_Movie/HDF/segmented.hdf5'
f = h5py.File(filename, 'r')

print ("Hdf5 file keys:\t{}".format(list(f.keys())))
print ("Hdf5 file vals:\t{}".format(list(f.values())))
print ()

# Access 'objects' details:
print ("List of members 'objects':\t{}".format(list(f['objects'])))

print ("Keys per 'objects':\t{}".format(list(f["objects"]["obj_type_2"].keys())))
print ("Vals per 'objects':\t{}".format(list(f["objects"]["obj_type_2"].values())))

print ("Keys per 'tracks':\t{}".format(list(f["tracks"]["obj_type_2"].keys())))
print ("Vals per 'tracks':\t{}".format(list(f["tracks"]["obj_type_2"].values())))

"""
# Learn how to create groups:
print (f.name)

filename = filename.replace(".hdf5", "_density.hdf5")
print (filename)


f = h5py.File(filename, 'a')
grp = f.create_group("subgroup")
print ("Hdf5 file keys:\t{}".format(list(f.keys())))
print ("Hdf5 file vals:\t{}".format(list(f.values())))
print ()


#with h5py.File(filename,  "a") as f:
del f['subgroup']

print (f.name)
print ("Hdf5 file keys:\t{}".format(list(f.keys())))
print ("Hdf5 file vals:\t{}".format(list(f.values())))
print ()


# Create 'density' key down the layer:
#del f['/objects/density']

print ("List of members 'objects':\t{}".format(list(f['objects'])))
print ("Keys per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].keys())))
print ("Vals per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].values())))

#subgroup = f.create_group('/objects/obj_type_2/density')

print ("List of members 'objects':\t{}".format(list(f['objects'])))
print ("Keys per 'objects':\t{}".format(list(f["objects"]["obj_type_2"].keys())))
print ("Vals per 'objects':\t{}".format(list(f["objects"]["obj_type_2"].values())))

print (list(f['objects']['obj_type_1']['density']))
"""



filename = '/Users/kristinaulicna/Documents/Rotation_2/Example_Movie/HDF/segmented_density.hdf5'

f = h5py.File(filename, 'r')
"""
map_seg = list(f['objects']['obj_type_2']['map'])
map_tra = list(f['tracks']['obj_type_2']['map'])
tracks = list(f['tracks']['obj_type_2']['tracks'])
dummies = list(f['tracks']['obj_type_2']['dummies'])

print (map_tra[0:10])
# [array([  0, 552], dtype=int32), array([ 552, 1030], dtype=int32), array([1030, 1484], dtype=int32), array([1484, 1934], dtype=int32), array([1934, 2382], dtype=int32), array([2382, 2827], dtype=int32), array([2827, 3265], dtype=int32), array([3265, 3703], dtype=int32), array([3703, 4140], dtype=int32), array([4140, 4576], dtype=int32)]

# Explore how to get the tracks for respective segmentation maps:
tracks = list(f['tracks']['obj_type_2']['tracks'])
track_random = list(f['tracks']['obj_type_2']['tracks'])[0:552]
coordinates = list(f['objects']['obj_type_2']['coords'])

#for item in track_random:
#    print (item, "\t", coordinates[item])
"""

tracks = list(f['tracks']['obj_type_2']['map'])
lst = []
for track in tracks:
    lst.append(int(track[1]) - int(track[0]))

import matplotlib.pyplot as plt
plt.hist(lst, bins=11)
plt.show()

"""
print (len(map_seg))
print (len(map_tra))
print (len(dummies))
print (len(tracks))
"""
