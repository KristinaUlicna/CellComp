import sys
sys.path.append("../")

from Movie_Analysis_Pipeline.Merging_Movie_Datasets.Find_Family_Class import FindFamily
from Cell_IDs_Analysis.Plotter_Lineage_Trees import PlotLineageTree

file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"

for line in open(file, "r"):
    line = line.rstrip().split("\t")
    if line[0] != "Cell_ID-posX-date":
        cell = line[0].split("-")[0]
        if int(cell) == 4682:
            root = FindFamily(cell_ID=line[0], filtered_file=file).FindRoot()
            print ("Cell: {}".format(line[0]))
            print ("Root: {}".format(root))

# Cell: 4682-pos2-17_07_31
# Root: [595, 'NaN', 0]

PlotLineageTree(root_ID=595, cell_ID=4682, show=True,
                xml_file="/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos2/tracks/tracks_type1.xml")
