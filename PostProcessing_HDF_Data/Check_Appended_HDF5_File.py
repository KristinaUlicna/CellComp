import h5py
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths


filename = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos0/HDF/segmented.hdf5"
f = h5py.File(filename, 'r')

print ("Hdf5 file keys:\t{}".format(list(f.keys())))
print ("Hdf5 file vals:\t{}".format(list(f.values())))
print ()

print ("List of members 'segmentation':\t{}".format(list(f['segmentation']["images"][0])))
print ("List of members 'segmentation':\t{}".format(len(f['segmentation']["images"])))
print ("List of members 'segmentation':\t{}".format(len(f['segmentation']["images"][0])))
print ("List of members 'segmentation':\t{}".format(len(f['segmentation']["images"][0][0])))

#print ("List of members 'tracks':\t{}".format(list(f['tracks'])))


# Access 'objects' details:
print ("List of members 'objects':\t{}".format(list(f['objects'])))

print ("Keys per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].keys())))
print ("Vals per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].values())))
print ("Elements per 'coords' RFP:\t{}".format(f["objects"]["obj_type_1"]["coords"]))
print ("Elements per 'coords' GFP:\t{}".format(f["objects"]["obj_type_1"]["coords"]))
print ("Elements per 'coords':\t{}".format(list(f["objects"]["obj_type_1"]["coords"][0:10])))
print ("Elements per 'density':\t{}".format(f["objects"]["obj_type_1"]["density"]))
print ("Elements per 'density':\t{}".format(list(f["objects"]["obj_type_1"]["density"][0:10])))
print ("Elements per 'labels':\t{}".format(f["objects"]["obj_type_1"]["labels"]))
print ("Elements per 'labels':\t{}".format(list(f["objects"]["obj_type_1"]["labels"][0:10])))
print ("Elements per 'map':\t{}".format(len(f["objects"]["obj_type_1"]["map"])))
print ("Elements per 'map':\t{}".format(list(f["objects"]["obj_type_1"]["map"][0:10])))

# Access 'tracks' details:
print ("List of members 'tracks':\t{}".format(list(f['tracks'])))

print("Keys per 'objects':\t{}".format(list(f["tracks"]["obj_type_1"].keys())))
print("Vals per 'objects':\t{}".format(list(f["tracks"]["obj_type_1"].values())))
print("Elements per 'fates':\t{}".format(f["tracks"]["obj_type_1"]["fates"]))
print("Elements per 'fates':\t{}".format(list(f["tracks"]["obj_type_1"]["fates"][0:10])))
print("Elements per 'tracks':\t{}".format(f["tracks"]["obj_type_1"]["tracks"]))
print("Elements per 'tracks':\t{}".format(list(f["tracks"]["obj_type_1"]["tracks"][0:10])))
print("Elements per 'map':\t{}".format(f["tracks"]["obj_type_1"]["map"]))
print("Elements per 'map':\t{}".format(list(f["tracks"]["obj_type_1"]["map"][0:10])))
print("Elements per 'LBEPRChChGen':\t{}".format(f["tracks"]["obj_type_1"]["LBEPRChChGen"]))
print("Elements per 'LBEPRChChGen':\t{}".format(list(f["tracks"]["obj_type_1"]["LBEPRChChGen"][0:10])))
print("Elements per 'LBEPR':\t{}".format(f["tracks"]["obj_type_1"]["LBEPR"]))
print("Elements per 'LBEPR':\t{}".format(list(f["tracks"]["obj_type_1"]["LBEPR"][0:10])))



if f.__bool__():
    f.close()

