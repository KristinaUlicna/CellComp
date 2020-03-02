from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths
from PostProcessing_HDF_Data.Process_LBEPR_Table_Append import AppendChChTime_ToLBEPR

movies = Get_MDCK_Movies_Paths()
for movie in movies:
    hdf5_file = movie + "HDF/segmented.hdf5"
    AppendChChTime_ToLBEPR(hdf5_file=hdf5_file)
    print ("Done for movie: {}".format(hdf5_file))
