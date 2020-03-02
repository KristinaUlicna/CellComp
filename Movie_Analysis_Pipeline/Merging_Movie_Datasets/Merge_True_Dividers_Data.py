# TODO: Write a txt_file which will contain all necessary information about the cell_ID:

import h5py
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths
from PostProcessing_HDF_Data.Process_LBEPR_Table_Class import Process_LBEPR_Table

def Extract_True_Dividers_Data(hdf5_file):
    """
    Data to extract:        [cell_ID (int), pos (str), date (str), cell_type (str), fate (int),
                             frm_st (int), frm_en (int), cct[min] (float), cct[hrs] (float),
                             gen (int), root (int), parent (int), child_1 (int), child_2 (int)]

    :param hdf5_file:
    :return:
    """

    true_cells = Process_LBEPR_Table(hdf5_file=hdf5_file, channel="GFP").ShortlistNonRootNonLeafCells()
    print (len(true_cells), true_cells[0:100])

    pos, date = hdf5_file.split("/")[-3], hdf5_file.split("/")[-4]
    data = []

    with h5py.File(hdf5_file, 'r') as f:
        for cell, fate in zip(f["tracks"]["obj_type_1"]["LBEPRChChGen"], f["tracks"]["obj_type_1"]["fates"]):
            if cell[0] in true_cells:
                frm_st = int(cell[1])
                frm_en = int(cell[2])
                cct = (frm_en - frm_st + 1) * 4
                l = [int(cell[0]), pos, date, "GFP", fate, frm_st, frm_en, cct, float(round(cct / 60), 2),
                     int(cell[7]), int(cell[4]), int(cell[3]), int(cell[5]), int(cell[6])]
                data.append(l)

    return data


def Write_Data_Into_TxtFile():
    """

    :param hdf5_file:
    :return:
    """

    txt_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/overall_analysis/cellIDdetails_MDCK_merged.txt"

    with open(txt_file, "w") as txt:
        movies = Get_MDCK_Movies_Paths()
        for movie in movies:
            print ("Processing movie: {}".format(movie))
            hdf5_file = movie + "HDF/segmented.hdf5"
            data = Extract_True_Dividers_Data(hdf5_file=hdf5_file)
            for lst in data:
                string = ""
                for element in lst:
                    string += str(element) + "\t"
                string = string[:-1] + "\n"
                txt.write(string)


Write_Data_Into_TxtFile()