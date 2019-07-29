# TODO: Create a 'cellIDdetails_merged_density.txt'

import sys
sys.path.append("../")

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


def MergeDensityData(exp_type = "MDCK_WT_Pure"):
    """ Merge all filtered data to a single txt.file,
        Change the cellID naming from current '1', '2', etc to '1-pos0-17_07_31'

    Args:
        exp_type (string); "MDCK_WT_Pure" by default    ->    cell type to be analysed

    Return:
        None.
        Writes a new file into the same directory as the exp_type specifies.
    """

    # Write a new file & initiate with header:
    merged_data_file = open("/Volumes/lowegrp/Data/Kristina/{}/cellIDdetails_merged_density.txt".format(exp_type), "w")
    header_list = ["Cell_ID-posX-date", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf",
                   "Den[0]", "Den[1/4]", "Den[1/2]", "Den[3/4]", "Den[-1]"]
    header_string = ""
    for item in header_list:
        header_string += str(item) + "\t"
    header_string = header_string[:-1]
    header_string += "\n"
    merged_data_file.write(header_string)

    # Iterate all server files:
    _, txt_file_list = GetMovieFilesPaths()

    for density_file in txt_file_list:
        density_file = density_file.replace("/analysis/cellIDdetails_raw.txt", "/density/cellIDdetails_density.txt")
        print("Filtered file (input): {}".format(density_file))
        filtered_file_name = str(density_file).split('/')
        for line in open(density_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] != "Cell_ID":
                line[0] = str(line[0]) + "-{}-{}".format(filtered_file_name[-3], filtered_file_name[-4])
                string = ""
                for item in line:
                    string += str(item) + "\t"
                string = string[:-1]
                string += "\n"
                merged_data_file.write(string)

    merged_data_file.close()


MergeDensityData(exp_type="MDCK_WT_Pure")