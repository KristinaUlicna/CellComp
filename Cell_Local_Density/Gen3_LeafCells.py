# TODO: Create a file with cells that would normally be in gen#3 but are leaves so are excluded from density analysis:

import sys
sys.path.append("../")

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths

_, txt_files_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")

new_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/pseudo_gen3_cellIDs.txt"
new_file = open(new_file, "w")


for file in txt_files_list:
    print(file)
    pos = file.split("/")[-3]
    date = file.split("/")[-4]
    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or len(line) < 8:
            continue
        if int(line[5]) == 3 and line[7] == "True":
            line[0] = "{}-{}-{}".format(str(line[0]), pos, date)
            string = ""
            for item in line:
                string += item + "\t"
            string = string[:-1]
            string += "\n"
            new_file.write(string)

new_file.close()