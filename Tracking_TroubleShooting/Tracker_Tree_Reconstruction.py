# TODO: Find out if you can reconstruct chopped trees from the tracker:

import sys
sys.path.append("../")

from Cell_IDs_Analysis.Plotter_Lineage_Trees import PlotLineageTree

raw_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/analysis/channel_RFP/cellIDdetails_raw.txt"
xml_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_type2.xml"

for line in open(raw_file, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 8:
        continue
    if int(line[5]) == 0 and line[7] == "False":
        print (line)
        PlotLineageTree(root_ID=int(line[0]), cell_ID=int(line[0]), xml_file=xml_file, show=True)
