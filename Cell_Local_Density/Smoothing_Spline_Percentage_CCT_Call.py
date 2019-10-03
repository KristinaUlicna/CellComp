#TODO: Run the smoothing spline function:

import sys
sys.path.append("../")

from Cell_Local_Density.Smoothing_Spline_Percentage_CCT_Function import SmoothDensity

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths

_, txt_file_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")

for txt_file in txt_file_list:
    date = txt_file.split("/")[-4]
    pos = txt_file.split("/")[-3]
    print("\tRunning the function for {}; {} density file.".format(date, pos))
    den_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/{}/{}/density/cellID_density.txt".format(date, pos)
    SmoothDensity(density_dict_txt_file=den_file)

SmoothDensity(density_dict_txt_file="/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos5/density/cellID_density.txt")