step = int((95900-88300+100)/100)
print (step)
a = list(range(88300, 95900, 77))
print (a[2])
a = [item / 100 for item in a]
print (a)
print (len(a))

import sys
sys.path.append("../")

from scipy.stats import linregress
from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


def Check100Percent(percentage=100):
    """

    :return:
    """
    _, txt_file_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")

    cct_hrs_list = []
    den_per_list = []

    for raw_file in txt_file_list:
        smoothed_density_file = raw_file.split("/")[:-2]
        smoothed_density_file = "/".join(smoothed_density_file) + "/density/cellID_density_smoothed.txt"
        print(smoothed_density_file)

        for line in open(smoothed_density_file, 'r'):
            line = line.rstrip().split("\t")
            if len(line) < 102:
                print (line[0])
            """
            if line[0] != "Cell_ID":
                print (int(line[0]))
                print (float(line[1]))
                print (float(line[percentage+1]))
                cct_hrs_list.append(float(line[1]))
                den_per_list.append(float(line[percentage+1]))
            """
    den_per_list = [item * 10000 for item in den_per_list]
    return cct_hrs_list, den_per_list

#Check100Percent(percentage=100)