from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths
from PostProcessing_HDF_Data.Process_LBEPR_Table_Class import Process_LBEPR_Table


movies = Get_MDCK_Movies_Paths()

counter = 0
for movie in movies:
    print("Movie: {}".format(movie))
    hdf5_file = movie + "HDF/segmented.hdf5"
    cells = Process_LBEPR_Table(hdf5_file=hdf5_file).ShortlistNonRootNonLeafCells(print_stats=True)
    counter += len(cells)

print ("Overall cells to analyse across MDCK dataset: {}".format(counter))
