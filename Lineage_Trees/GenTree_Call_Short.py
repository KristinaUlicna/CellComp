# ----- LineageTree Creator CLASS Calling -----

from GenTree_Class_Short import ProcessTrackedMovies

cell_ID_list = [103, 1960, 7158, 11388, 11531, 11582, 12015]
cell_ID_name = 'Node_8_Tree_short'

cell_ID_list = [98, 99, 100, 101, 102, 198, 199, 200, 201, 202]
cell_ID_name = 'Over_100_short'

call = ProcessTrackedMovies()
#call.PrintDetailsTable(cell_ID_list = cell_ID_list)
call.StoreDetailsFile(cell_ID_list = cell_ID_list, file_name_suffix = cell_ID_name)
