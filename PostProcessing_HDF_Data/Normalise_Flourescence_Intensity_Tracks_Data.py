import h5py
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


class Signal_Intensity(object):

    def __init__(self, hdf5_file):

        self.hdf5_file = hdf5_file



with h5py.File(hdf5_file, 'r') as f:
    for cell in range(0, 100):

        if cell % 20 == 0:
            print ("Plotting for cell #{}...".format(cell))

        cell_map = f["tracks"]["obj_type_2"]["map"][cell]
        #print (cell_map)
        cell_tracks = f["tracks"]["obj_type_2"]["tracks"][cell_map[0]:cell_map[1]]
        #print (cell_tracks)

        # Extract raw density data:
        cell_frame = []
        fluo_signal = []
        for track in cell_tracks:
            if int(track) > 0:
                cell_frame.append(int(f["objects"]["obj_type_2"]["coords"][track][0]))
                fluo_signal.append(float(f["objects"]["obj_type_2"]["density"][track][4]))

        # Perform smoothing spline fit with different degrees of 's' = positive smoothing factor to choose number of knots
        n = 0
        """
        for s_degree in range(0, 6):
            s = UnivariateSpline(x=cell_frame, y=fluo_signal, s=s_degree)
            print ("Smoothing spline fit with s = {} -> {}".format(s_degree, s(cell_frame)))
            plt.plot(cell_frame[n:len(cell_frame)-n], s(cell_frame[n:len(cell_frame)-n]), label="s = {}".format(s_degree))
        """

        # Plot the thing:
        plt.scatter(x=cell_frame[n:len(cell_frame)-n], y=fluo_signal[n:len(cell_frame)-n], s=2, alpha=0.5)

    plt.title("Raw Fluorescence Intensity Data [10%:80%:10%]")
    plt.xlabel("Frame #")
    plt.ylabel("Average Fluorescence Intensity")
    plt.legend(loc='best')
    plt.show()
    plt.close()

# ------------


# Call the stuff:
hdf5_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/HDF/segmented.hdf5"


