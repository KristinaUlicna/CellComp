# TASK: Exploring the new structure of the HDF file after the September update.

"""


                                      'coords'
                                       |                ... shape (320272, 5) = total number of observations per movie;
                                       |                                      [t (frame), x, y, z, type (1=GFP, 2=RFP)]
                     'obj_type_1'------o---- 'map'      ... shape (320272, 6) = total number of observations per movie;
                       |          |    |                                      [_, _, _, _, _, _] -> softmax probability
                       |          |    |                ... shape (1105, 2) = length of the movie
                       |          |   'labels'                                [_, _] -> starting & finishing cell count
          'objects'----o          |
            |          |           ---- 'density_raw' & 'density_smooth'
            |          |                     & TODO: 'neighbourhood'
            |          |
            |        'obj_type_2'----- ... ditto
            |
            |
        ----o
            |                         'dummies'
            |                          |
            |        'obj_type_1'------o---- 'map'
            |          |               |
            |          |              'tracks'
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


filename = '/Users/kristinaulicna/Documents/Rotation_2/Example_Movie/HDF/segmented.hdf5'
f = h5py.File(filename, 'r')

print ("Hdf5 file keys:\t{}".format(list(f.keys())))
print ("Hdf5 file vals:\t{}".format(list(f.values())))
print ()

# Access 'objects' details:
print ("List of members 'objects':\t{}".format(list(f['objects'])))

print ("Keys per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].keys())))
print ("Vals per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].values())))
print ("Elements per 'coords':\t{}".format(f["objects"]["obj_type_1"]["coords"]))
print ("Elements per 'coords':\t{}".format(list(f["objects"]["obj_type_1"]["coords"][0:10])))
print ("Elements per 'labels':\t{}".format(f["objects"]["obj_type_1"]["labels"]))
print ("Elements per 'labels':\t{}".format(list(f["objects"]["obj_type_1"]["labels"][0:10])))
print ("Elements per 'map':\t{}".format(f["objects"]["obj_type_1"]["map"]))
print ("Elements per 'map':\t{}".format(list(f["objects"]["obj_type_1"]["map"][0:10])))

# Access 'tracks' details:
print ("List of members 'tracks':\t{}".format(list(f['tracks'])))

print("Keys per 'objects':\t{}".format(list(f["tracks"]["obj_type_1"].keys())))
print("Vals per 'objects':\t{}".format(list(f["tracks"]["obj_type_1"].values())))
print("Elements per 'dummies':\t{}".format(f["tracks"]["obj_type_1"]["dummies"]))
print("Elements per 'dummies':\t{}".format(list(f["tracks"]["obj_type_1"]["dummies"][0:10])))
print("Elements per 'tracks':\t{}".format(f["tracks"]["obj_type_1"]["tracks"]))
print("Elements per 'tracks':\t{}".format(list(f["tracks"]["obj_type_1"]["tracks"][0:10])))
print("Elements per 'map':\t{}".format(f["tracks"]["obj_type_1"]["map"]))
print("Elements per 'map':\t{}".format(list(f["tracks"]["obj_type_1"]["map"][0:10])))


