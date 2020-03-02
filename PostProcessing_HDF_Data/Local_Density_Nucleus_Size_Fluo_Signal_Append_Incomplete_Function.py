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
from PostProcessing_HDF_Data.Local_Density_Nucleus_Size_Fluo_Signal_Create_Class import Local_Density_Nucleus_Size_Fluo_Signal


def CreateHDF5Dataset_Density(hdf5_file):
    """ Create an array which you will append to the existing 'LBEPR' table.
        shape = len(lbepr, 3); [child_1, child_2, generation]
    """

    # Call the class & its relevant functions:
    call = Local_Density_Nucleus_Size_Fluo_Signal(hdf5_file=hdf5_file)
    density, nucleus, fsignal = call.Process_Whole_Movie(local_density=True,
                                                         nucleus_size=True,
                                                         fluo_signal=True)

    # Create a list of lists with data, return in np.array form:
    maxi_list = []
    for den, nuc, sig in zip(density, nucleus, fsignal):
        lst = [den, .0, nuc, .0, sig, .0]
        maxi_list.append(lst)

    raw_data = np.array(maxi_list, dtype=np.float64)
    return raw_data



def AppendDensityDataset(hdf5_file):
    """ "LBEPR" shape (X, 5)    ->    "LBEPRChChGen" shape (X, 8) """

    raw_data = CreateHDF5Dataset_Density(hdf5_file=hdf5_file)

    # Open the HDF5 file & do dataset dimensions check:
    f = h5py.File(hdf5_file, 'a')
    coords = len(f["objects"]["obj_type_1"]["coords"])

    # Check for shape of the 'coords' & data being appended to the 'density' dataset:
    if raw_data.shape[0] != coords or raw_data.shape[1] != 6:
        raise ValueError("Dimensions of 'density' dataset to appended <{}> doesn't match the coordinates length <{}>"
                          .format(raw_data.shape, coords))

    # Append:
    if "density" in list(f["objects"]["obj_type_1"]):
        del f["objects"]["obj_type_1"]["density"]

    grp = f["objects"]["obj_type_1"]
    grp.create_dataset(name="density", data=raw_data)

    if f.__bool__():
        f.close()



# Call the class to create the local_density, nucleus_size & fluo_intensity vectors:
hdf5_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos0/HDF/segmented.hdf5"
AppendDensityDataset(hdf5_file=hdf5_file)

