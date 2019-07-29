import sys
sys.path.append("../")

from Cell_Cycle_Duration.Find_Family_Class import FindFamily

file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged_density.txt"


# Find parents of all generation#1 cells:

parent_list = []
parent_frm_st = []
for line in open(file, "r"):
    line = line.rstrip().split("\t")
    if line[0] != "Cell_ID-posX-date":
        if int(line[5]) == 1:
            pos = line[0].split("-")[-2]
            date = line[0].split("-")[-1]
            parent = FindFamily(cell_ID=line[0], filtered_file=file).FindParent()
            parent = str(parent[0]) + "-{}-{}".format(pos, date)
            parent_list.append(parent)
            pos = line[0].split("-")[-2]
            date = line[0].split("-")[-1]
            raw_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/{}/{}/analysis/cellIDdetails_raw.txt".format(date, pos)
            for cell in open(raw_file, "r"):
                cell = cell.rstrip().split("\t")
                if cell[0] == "Cell_ID" or len(cell) < 8:
                    continue
                if int(cell[0]) == int(parent.split("-")[0]):
                    parent_frm_st.append(int(cell[1]))


print ("Parent CellID list: len = {}; {}".format(len(parent_list), parent_list))
print (type(parent_list[0]))


# Write the generation#0 cell_ID details into a separate file, maintaining the pos & date:

new_gen_0_file = "/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_parents_gen0.txt"
new_gen_0_file = open(new_gen_0_file, "w")
header = ["Cell_ID-posX-date", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]
header_string = ""
for item in header:
    header_string += str(item) + "\t"
header_string = header_string[:-1]
header_string += "\n"
new_gen_0_file.write(header_string)

for item in parent_list:
    cellid = item.split("-")[-3]
    pos = item.split("-")[-2]
    date = item.split("-")[-1]

    file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/{}/{}/analysis/cellIDdetails_raw.txt".format(date, pos)
    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or len(line) < 8:
            continue
        string = ""
        if int(line[0]) == int(cellid):
            line[0] = str(line[0]) + "-{}-{}".format(pos, date)
            for element in line:
                string += str(element) + "\t"
            string = string[:-1]
            string += "\n"
        new_gen_0_file.write(string)

new_gen_0_file.close()