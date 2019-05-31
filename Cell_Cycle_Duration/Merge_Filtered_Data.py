# TODO: Merge all filtered data to a single txt.file,
# TODO: Change the cellID naming from current '1', '2', etc to '1-pos0-17_07_31'

import sys
sys.path.append("../")

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


def MergeFilteredData(exp_type = "MDCK_WT_Pure"):
    """ Merge all filtered data to a single txt.file,
        Change the cellID naming from current '1', '2', etc to '1-pos0-17_07_31'
    Args:
        exp_type (string); "MDCK_WT_Pure" by default    ->    cell type to be analysed

    Return:
        None.
        Writes a new file into the same directory as the exp_type specifies.
    """

    # Write a new file & initiate with header:
    merged_data_file = open("/Volumes/lowegrp/Data/Kristina/{}/cellIDdetails_merged.txt".format(exp_type), "w")
    header_list = ["Cell_ID-posX-date", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]
    header_string = ""
    for item in header_list:
        header_string += str(item) + "\t"
    header_string = header_string[:-1]
    header_string += "\n"
    merged_data_file.write(header_string)

    # Iterate all server files:
    _, txt_file_list = GetMovieFilesPaths()

    for filtered_file in txt_file_list:
        filtered_file = filtered_file.replace("raw", "filtered")
        #print("Filtered file (input): {}".format(filtered_file))
        filtered_file_name = str(filtered_file).split('/')
        for line in open(filtered_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID":
                continue
            line[0] = str(line[0]) + "-{}-{}".format(filtered_file_name[-3], filtered_file_name[-4])
            string = ""
            for item in line:
                string += str(item) + "\t"
            string = string[:-1]
            string += "\n"
            merged_data_file.write(string)

    merged_data_file.close()


MergeFilteredData(exp_type="MDCK_WT_Pure")