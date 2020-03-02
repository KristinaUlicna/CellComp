# TODO: Access the information in the segmented.hdf5 file: especially the positions of the cell centres at every frame

import h5py
import matplotlib.pyplot as plt

filename = '/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/HDF/segmented.hdf5'
f = h5py.File(filename, 'r')

print ("Hdf5 file keys:\t\t{}".format(list(f.keys())))       # to list the individual keys
print ("Hdf5 file values:\t{}".format(list(f.values())))     # summary, e.g number of members (here, 1105)...
print ("List of members:\t{}".format(len(list(f['frames']))))     # list of how the 1105 members are called

# Access data in ['frames_0']
print ("Keys per frame:\t{}".format(list(f["frames"]["frame_0"].keys())))
print ("Values per frame:\t{}".format(list(f["frames"]["frame_0"].values())))

# Access data in ['coords', 'labels']:
print ("'Coords' per frame:\t{}".format(f["frames"]["frame_0"]["coords"]))
print ("'Coords' per frame:\t{}".format(list(f["frames"]["frame_0"]["coords"])))            # [t (frame), x, y, z, type (1=GFP, 2=RFP)]
print ("'Coords' per frame:\t{}".format(len(list(f["frames"]["frame_0"]["coords"]))))       # len = 216 (both GFP & RFP)

print ("'Labels' per frame:\t{}".format(f["frames"]["frame_0"]["labels"]))
print ("'Labels' per frame:\t{}".format(list(f["frames"]["frame_0"]["labels"])))
print ("'Labels' per frame:\t{}".format(len(list(f["frames"]["frame_0"]["labels"]))))

x = list(range(0, 1105))
y = []
for number in x:
    cell_count = len(list(f["frames"]["frame_{}".format(number)]["labels"]))
    y.append(cell_count)

plt.scatter(x, y)
plt.title("Cell count according to 'segmented.hdf5'")
plt.xlabel("Frame #")
plt.ylabel("Event count")
plt.grid(which='major')
#plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Tracker_Evaluation/Cell_Count.jpeg", bbox_inches="tight")
plt.show()
plt.close()