import h5py
import numpy as np
from PostProcessing_HDF_Data.Process_LBEPR_Table_Class import Process_LBEPR_Table



def CreateHDF5Dataset_ChChGen(hdf5_file):
    """ Create an array which you will append to the existing 'LBEPR' table.
        shape = len(lbepr, 3); [child_1, child_2, generation]
    """

    # Call the class & its relevant functions:
    call = Process_LBEPR_Table(hdf5_file=hdf5_file, channel="GFP")
    children = call.FindBothChildrenOfParent()
    generation = call.FindGenerationalDepth()

    # Create a list of lists with data, return in np.array form:
    maxi_list = []
    for child_list, gen in zip(children, generation):
        child_list.append(gen)
        maxi_list.append(child_list)

    chchtime = np.array(maxi_list, dtype=np.int32)
    return chchtime


def AppendChChTime_ToLBEPR(hdf5_file):
    """ "LBEPR" shape (X, 5)    ->    "LBEPRChChGen" shape (X, 8) """

    chchtime_array = CreateHDF5Dataset_ChChGen(hdf5_file=hdf5_file)

    # Open the HDF5 file:
    f = h5py.File(hdf5_file, 'a')
    lbepr_array = list(f["tracks"]["obj_type_1"]["LBEPR"])

    lst = []
    for item, add in zip(lbepr_array, chchtime_array):
        lst.append(np.append(item, add))
    full_array = np.array(lst, dtype=np.int32)

    if len(lbepr_array) != full_array.shape[0]:
        raise ValueError("The shapes of LBEPR and LBEPRChChGen arrays are different.")

    # Append to HDF5:
    if "LBEPRChChGen" in list(f["tracks"]["obj_type_1"]):
        del f["tracks"]["obj_type_1"]["LBEPRChChGen"]

    grp = f["tracks"]["obj_type_1"]
    grp.create_dataset(name="LBEPRChChGen", data=full_array)

    if f.__bool__():
        f.close()


def DeleteLBEPR_KeepLBEPRChChGen(hdf5_file):
    """ Not necessary to call. But just in case you don't want data duplicates. """

    # Open the HDF5 file:
    f = h5py.File(hdf5_file, 'a')
    lbepr = f["tracks"]["obj_type_1"]["LBEPR"]
    lbeprchchgen = f["tracks"]["obj_type_1"]["LBEPRChChGen"]

    # Delete only if replicas of each other:
    if lbepr.shape[0] == lbeprchchgen.shape[0]:
        if lbepr.shape[1] == 5 and lbeprchchgen.shape[1] == 8:
            del f["tracks"]["obj_type_1"]["LBEPR"]
