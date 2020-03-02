# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
# ----- POST-PROCESSING OF HDF FILES: APPENDING DATA OF ----- #
#       LOCAL CELL DENSITY, NUCLEUS SIZE & DNA CONTENT        #
#       FROM FLUORESCENCE SIGNAL INTENSITY                    #
#                                                             #
# ----- Creator:            Kristina ULICNA             ----- #
#                                                             #
# ----- Last updated:       31th Jan 2020               ----- #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import h5py
import numpy as np
from PostProcessing_HDF_Data.Local_Density_Nucleus_Size_Fluo_Signal_Smooth_Class import Smooth_or_Scale_Raw_Data


def CreateHDF5Dataset_Density(hdf5_file):
    """ Create an array which you will append to the existing 'LBEPR' table.
        shape = len(lbepr, 3); [child_1, child_2, generation]
    """

    # Call the classes & their relevant functions:
    call = Smooth_or_Scale_Raw_Data(hdf5_file=hdf5_file)
    raw_density, smooth_density = call.Smooth_Data(which_data="density")
    raw_nucleus, smooth_nucleus = call.Smooth_Data(which_data="nucleus")
    raw_fsignal, smooth_fsignal = call.Smooth_Data(which_data="fsignal")

    raw_scaled_fluo = call.Scale_Fluo_Signal_Interphase(which_data="raw")
    smooth_scaled_fluo = call.Scale_Fluo_Signal_Interphase(which_data="smooth")

    # Check lengths:
    if len(raw_density) != len(smooth_density) != len(raw_nucleus) != len(smooth_nucleus) \
            != len(raw_fsignal) != len(smooth_fsignal) != len(raw_scaled_fluo) != len(smooth_scaled_fluo):
        raise ValueError("Data of different lengths!")

    # Create a list of lists with data, return in np.array form:
    # TODO: Do this better! Transpose?
    maxi_list = []
    for a, b, c, d, e, f, g, h in zip(raw_density, smooth_density,
                                      raw_nucleus, smooth_nucleus,
                                      raw_fsignal, smooth_fsignal,
                                      raw_scaled_fluo, smooth_scaled_fluo):
        lst = [a, b, c, d, e, f, g, h]
        maxi_list.append(lst)

    data = np.array(maxi_list, dtype=np.float64)
    return data



def AppendDensityDataset(hdf5_file):
    """ """

    raw_data = CreateHDF5Dataset_Density(hdf5_file=hdf5_file)

    # Open the HDF5 file & do dataset dimensions check:
    f = h5py.File(hdf5_file, 'a')
    coords = len(f["objects"]["obj_type_1"]["coords"])

    # Check for shape of the 'coords' & data being appended to the 'density' dataset:
    if raw_data.shape[0] != coords or raw_data.shape[1] != 8:
        raise ValueError("Dimensions of 'density' dataset to appended <{}> doesn't match the coordinates length <{}>"
                          .format(raw_data.shape, coords))

    # Append:
    if "density" in list(f["objects"]["obj_type_1"]):
        del f["objects"]["obj_type_1"]["density"]

    grp = f["objects"]["obj_type_1"]
    grp.create_dataset(name="density", data=raw_data)

    if f.__bool__():
        f.close()


"""
# Call the class to create the local_density, nucleus_size & fluo_intensity vectors:
hdf5_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos0/HDF/segmented.hdf5"
AppendDensityDataset(hdf5_file=hdf5_file)
"""