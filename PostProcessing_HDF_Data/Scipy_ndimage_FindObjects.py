import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, find_objects


hdf5_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/HDF/segmented.hdf5"

hdf5_file = h5py.File(hdf5_file, 'r')
pixels = hdf5_file["segmentation"]["images"][0]

plt.imshow(X=pixels)    # plots a 2D array straight ahead!
plt.show()
plt.close()

object_labels, num_features = label(input=pixels)
print (object_labels)
print (type(object_labels))

plt.imshow(X=object_labels)  # plots a 2D array straight ahead!
plt.show()
plt.close()

found_objects = find_objects(object_labels)
print (found_objects)
print (len(found_objects))

print ("Is it true?", num_features == len(found_objects))
# (slice(edge_start (integer), edge_right (integer), edge_depth (None) on the 'row'), slice(edge_start (integer), edge_right (integer), edge_depth (None) on the 'column'))

loc = find_objects(object_labels)[33]
print (loc)
print (object_labels[loc])

a = np.array([0, 3, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0, 1, 3, 4])
unique, counts = np.unique(a, return_counts=True)
print (unique)
print (counts)