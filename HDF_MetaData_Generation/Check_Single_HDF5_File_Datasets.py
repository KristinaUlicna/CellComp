import os
import h5py
import matplotlib.pyplot as plt
#from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths

filename = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/AB0327/pos0/HDF/segmented.hdf5"
#filename = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/AB0327/pos0/HDF/segmented.hdf5"

print (filename)
print ("Does server path exist? {}".format(os.path.exists("/Volumes/lowegrp/")))


f = h5py.File(filename, 'r')

print ("Hdf5 file keys:\t{}".format(list(f.keys())))
print ("Hdf5 file vals:\t{}".format(list(f.values())))
print ("Hdf5 file vals:\t{}".format(len(list(f.values())[0])))

print ()

#print ("List of members 'segmentation':\t{}".format(list(f['segmentation']["images"][0])))
print ("List of members 'segmentation':\t{}".format(len(f['segmentation']["images"])))
print ("List of members 'segmentation':\t{}".format(len(f['segmentation']["images"][0])))
print ("List of members 'segmentation':\t{}".format(len(f['segmentation']["images"][0][0])))


plt.imshow(X=list(f['segmentation']["images"][-1]))  # plots a 2D array straight ahead!
plt.imsave(fname=filename.replace("segmented.hdf5", "frm_last.png"), arr=list(f['segmentation']["images"][-1]))
plt.title("Raw Segmented Binary Mask at frame #0")
plt.show()
plt.close()


#print ("List of members 'tracks':\t{}".format(list(f['tracks'])))


# Access 'objects' details:
print ("List of members 'objects':\t{}".format(list(f['objects'])))

print ("Keys per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].keys())))
print ("Vals per 'objects':\t{}".format(list(f["objects"]["obj_type_1"].values())))
print ("Elements per 'coords' GFP:\t{}".format(f["objects"]["obj_type_1"]["coords"]))
print ("Elements per 'coords' GFP:\t{}".format(list(f["objects"]["obj_type_1"]["coords"][-2:])))
print ("Elements per 'coords' RFP:\t{}".format(f["objects"]["obj_type_2"]["coords"]))
print ("Elements per 'coords' RFP:\t{}".format(list(f["objects"]["obj_type_2"]["coords"][-2:])))

print ("Elements per 'local_density':\t{}".format(f["objects"]["obj_type_1"]["local_density"]))
print ("Elements per 'local_density':\t{}".format(list(f["objects"]["obj_type_1"]["local_density"][-2:])))
# [0.00033398477261539105, 0.0004301657065047774, 0.0016427682128688458, 0.0013724213862169466, 0.002308157826605753, 0.000660454520404482, 0.0017822748026707106, 0.0023343192281471887, 0.0004422734179053625, 0.0010281609728783106]
print ("Elements per 'nucleus_size':\t{}".format(f["objects"]["obj_type_1"]["nucleus_size"]))
print ("Elements per 'nucleus_size':\t{}".format(list(f["objects"]["obj_type_1"]["nucleus_size"][-2:])))
# [9.0, 9.0, 5.0, 5.0, 15.0, 15.0, 14.0, 14.0, 10.0, 10.0]
print ("Elements per 'fluo_signal_sum':\t{}".format(f["objects"]["obj_type_1"]["fluo_signal_sum"]))
print ("Elements per 'fluo_signal_sum':\t{}".format(list(f["objects"]["obj_type_1"]["fluo_signal_sum"][-2:])))
# [349.0, 361.0, 600.0, 481.0, 378.0, 114.0, 198.0, 547.0, 236.0, 230.0]

print ("Elements per 'labels':\t{}".format(f["objects"]["obj_type_1"]["labels"]))
print ("Elements per 'labels':\t{}".format(list(f["objects"]["obj_type_1"]["labels"][-1])))
print ("Elements per 'map':\t{}".format(len(f["objects"]["obj_type_1"]["map"])))
print ("Elements per 'map':\t{}".format(list(f["objects"]["obj_type_1"]["map"][-1])))

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
print("Elements per 'LBEPR':\t{}".format(f["tracks"]["obj_type_1"]["LBEPR"]))
print("Elements per 'LBEPR':\t{}".format(list(f["tracks"]["obj_type_1"]["LBEPR"][0:10])))
print("Elements per 'Ch_Ch_Gen_CCT':\t{}".format(f["tracks"]["obj_type_1"]["Ch_Ch_Gen_CCT"]))
print("Elements per 'Ch_Ch_Gen_CCT':\t{}".format(list(f["tracks"]["obj_type_1"]["Ch_Ch_Gen_CCT"][0:10])))



if f.__bool__():
    f.close()

