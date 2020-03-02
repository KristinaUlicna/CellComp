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


from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths
from PostProcessing_HDF_Data.Local_Density_Nucleus_Size_Fluo_Signal_Append_Incomplete_Function import AppendDensityDataset as call_1
from PostProcessing_HDF_Data.Local_Density_Nucleus_Size_Fluo_Signal_Append_Complete_Function import AppendDensityDataset as call_2

movies = Get_MDCK_Movies_Paths()
for movie in movies:
    print ("Movie: {}".format(movie))
    hdf5_file = movie + "HDF/segmented.hdf5"
    call_1(hdf5_file=hdf5_file)
    call_2(hdf5_file=hdf5_file)


"""
# Call the class to create the local_density, nucleus_size & fluo_intensity vectors:
hdf5_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos0/HDF/segmented.hdf5"
AppendDensityDataset(hdf5_file=hdf5_file)
"""