import h5py
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


hdf5_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/HDF/segmented.hdf5"

with h5py.File(hdf5_file, 'r') as f:
    cell_map = f["tracks"]["obj_type_2"]["map"][0]
    print (cell_map)
    cell_tracks = f["tracks"]["obj_type_2"]["tracks"][cell_map[0]:cell_map[1]]
    print (cell_tracks)

    # Extract raw density data:
    cell_frame = []
    cell_nucleus = []
    for track in cell_tracks:
        if int(track) > 0:
            cell_frame.append(int(f["objects"]["obj_type_2"]["coords"][track][0]))
            cell_nucleus.append(float(f["objects"]["obj_type_2"]["density"][track][2]))
        #else:
        #    cell_frame.append(None)
        #    cell_density.append(None)

    print(cell_nucleus)

    # Perform smoothing spline fit with different degrees of 's' = positive smoothing factor to choose number of knots
    for s_degree in range(0, 2):
        s = UnivariateSpline(x=cell_frame, y=cell_nucleus, s=s_degree)
        print ("Smoothing spline fit with s = {} -> {}".format(s_degree, s(cell_frame)))
        plt.plot(cell_frame, s(cell_frame), label="s = {}".format(s_degree))

    # Plot the thing:
    plt.scatter(x=cell_frame, y=cell_nucleus, s=2, c="black", label="Data")
    plt.title("Smoothing the nucleus size data")
    plt.xlabel("Frame #")
    plt.ylabel("Nucleus Size")
    plt.legend(loc='best')
    plt.show()
    plt.close()

# ------------
