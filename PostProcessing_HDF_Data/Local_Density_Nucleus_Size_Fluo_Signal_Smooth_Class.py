import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from PostProcessing_HDF_Data.Local_Density_Nucleus_Size_Fluo_Signal_Create_Class import Local_Density_Nucleus_Size_Fluo_Signal


class Smooth_or_Scale_Raw_Data(object):

    def __init__(self, hdf5_file):

        # Open the hdf5_file to source track information from it:
        self.hdf5_file = h5py.File(hdf5_file, 'r')
        self.obj = self.hdf5_file["objects"]["obj_type_1"]
        self.trk = self.hdf5_file["tracks"]["obj_type_1"]
        dataset_size = self.obj["coords"].shape[0]

        try:
            # QUICK: extract data directly from HDF5 file:
            data = np.array(self.obj["density"]).T.tolist()
            self.raw_den, self.raw_nuc, self.raw_sig = data[0], data[2], data[4]
            print (self.raw_den[0:100])
            print (len(self.raw_den))
            print (self.raw_nuc[0:100])
            print (len(self.raw_nuc))
            print (self.raw_sig[0:100])
            print (len(self.raw_sig))

            print ("Data extracted from HDF5 file.")

        except:
            # SLOW: Call the class to return 3 raw data vectors:
            call = Local_Density_Nucleus_Size_Fluo_Signal(hdf5_file=hdf5_file)
            self.raw_den, self.raw_nuc, self.raw_sig = call.Process_Whole_Movie \
                    (local_density=True, nucleus_size=True, fluo_signal=True)
            print ("Data created from scratch.")

        # Sanity check:
        if len(self.raw_den) != len(self.raw_nuc) != len(self.raw_sig) != dataset_size:
            raise ValueError("Dimensions of returned created den <{}> & nuc <{}> & sig <{}> arrays are not matching."
                             .format(len(self.raw_den), len(self.raw_nuc), len(self.raw_sig)))

        # Initialise yet empty lists to return later:
        self.smooth_data = [0.0 for _ in range(dataset_size)]
        self.scaled_fluo = [0.0 for _ in range(dataset_size)]


    def Smooth_Data(self, which_data, show=False):
        """ """

        if which_data == "density":
            source = self.raw_den
        elif which_data == "nucleus":
            source = self.raw_nuc
        elif which_data == "fsignal":
            source = self.raw_sig
        else:
            raise Exception("Specify which dataset you want to process under 'which_data' argument: "
                            "'density' or 'nucleus' or 'fsignal'")

        # Process all tracks: remember, there will be a different number of tracks to number of movie frames...
        for enum, track_reference in enumerate(self.trk["map"]):

            if enum % 200 == 0:
                print ("Smoothing the <{}> data for track #{} out of {} tracks..."
                       .format(which_data, enum, len(self.trk["map"])))

            cell_track = []
            cell_frame = []
            cell_raw_data = []
            for track in self.trk["tracks"][track_reference[0]:track_reference[1]]:

                # This is a check for dummy objects: they don't have raw density!
                if track > 0:
                    value = source[track]
                    if value != 0:
                        cell_track.append(track)
                        cell_raw_data.append(value)
                        cell_frame.append(self.obj["coords"][track][0])

            # Univariate spline can only be applied on 3+ data points: check for that, if not, return raw values
            if len(cell_raw_data) > 3:
                # Fit with different degrees of 's' = 1 (= positive smoothing factor to choose number of knots)
                s = UnivariateSpline(x=cell_frame, y=cell_raw_data, s=1)
                smooth_data = s(cell_frame)
            else:
                # Return a list which contains just the raw, unaltered data:
                smooth_data = cell_raw_data

            # Sanity Check:
            if len(cell_track) != len(smooth_data):
                raise ValueError("Omg!")

            for track, s_value in zip(cell_track, smooth_data):
                self.smooth_data[track] = s_value

            # Plot if you want to:
            if show is True:
                cell_ID = self.trk["LBEPR"][enum][0]
                plt.plot(cell_frame, smooth_data, color="orange", label="Smoothened Data")
                plt.scatter(x=cell_frame, y=cell_raw_data, s=8, c="purple", label="Raw Data")
                plt.title("Smoothing the cell {} data for cell_ID #{}".format(which_data, cell_ID))
                plt.xlabel("Frame #")
                plt.ylabel("Cell Density")
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
                plt.show()
                plt.close()

        return source, self.smooth_data


    def Scale_Fluo_Signal_Interphase(self, which_data, show=False):

        if which_data == "raw":
            source = self.raw_sig
        elif which_data == "smooth":
            _, source = self.Smooth_Data(which_data="fsignal")
        else:
            raise Exception("Specify which dataset you want to normalise under 'which_data' argument: "
                            "'raw' or 'smooth'")

        # Process all tracks: remember, there will be a different number of tracks to number of movie frames...
        for enum, track_reference in enumerate(self.trk["map"]):

            if enum % 200 == 0:
                print("Scaling <{}> data for track #{} out of {} tracks..."
                      .format(which_data, enum, len(self.trk["map"])))

            cell_track = []
            cell_frame = []
            cell_raw_data = []

            for track in self.trk["tracks"][track_reference[0]:track_reference[1]]:

                if track > 0:                                   # exclude 'dummy' objects
                    fluo = source[track]
                    classif = self.obj["labels"][track][0]      # 0 = interphase ?
                    if fluo != 0.0 and classif == 0.0:
                        cell_track.append(track)
                        cell_raw_data.append(fluo)
                        cell_frame.append(self.obj["coords"][track][0])

            # Min-max normalisation equation: zi = (xi - x.min) / (x.max - x.min)
            normalised = cell_raw_data
            if len(cell_raw_data) > 1:
                min = np.min(cell_raw_data)
                max = np.max(cell_raw_data)
                normalised = [(x - min) / (max - min) for x in cell_raw_data]

            # Sanity Check:
            if len(cell_track) != len(normalised):
                raise ValueError("Omg!")

            for track, norm in zip(cell_track, normalised):
                self.scaled_fluo[track] = norm

            # Plot if you want to:
            if show is True:
                cell_ID = self.trk["LBEPR"][enum][0]
                plt.plot(cell_frame, normalised, color="forestgreen", label="Normalised Data")
                plt.title("Smoothing the cell {} data for cell_ID #{}".format(which_data, cell_ID))
                plt.xlabel("Frame #")
                plt.ylabel("Cell Density")
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
                plt.show()
                plt.close()

        return self.scaled_fluo


    def __exit__(self):
        self.hdf5_file.close()



# Call the class to check correctness:
hdf5_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos12/HDF/segmented.hdf5"
call = Smooth_or_Scale_Raw_Data(hdf5_file=hdf5_file)

den_raw, den_smooth = call.Smooth_Data(which_data="density")
print (len(den_raw), den_raw[0:100])
print (len(den_smooth), den_smooth[0:100])

nuc_raw, nuc_smooth = call.Smooth_Data(which_data="nucleus")
print (len(nuc_raw), nuc_raw[0:100])
print (len(nuc_smooth), nuc_smooth[0:100])

sig_raw, sig_smooth = call.Smooth_Data(which_data="fsignal")
print (len(sig_raw), sig_raw[0:100])
print (len(sig_smooth), sig_smooth[0:100])

