dir = "/Volumes/lowegrp/Data/Alan/Anna_to_process/2017_02_28/pos16/tracks/"

gfp_file = "tracks_type1.xml"
rfp_file = "tracks_type2.xml"

import sys
sys.path.append("../")

from Cell_IDs_Analysis.Extractor_CellIDdetails_Class import GetCellDetails

#GetCellDetails(xml_file=dir + gfp_file).IterateTrees()
#GetCellDetails(xml_file=dir + rfp_file).IterateTrees()

raw_gfp = "/Volumes/lowegrp/Data/Alan/Anna_to_process/2017_02_28/pos16/analysis/channel_GFP/cellIDdetails_raw.txt"
raw_rfp = "/Volumes/lowegrp/Data/Alan/Anna_to_process/2017_02_28/pos16/analysis/channel_RFP/cellIDdetails_raw.txt"

counter_gfp = 0
counter_rfp = 0

for line in open(raw_gfp, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 8:
        continue
    if int(line[5]) != 0:
        counter_gfp += 1

for line in open(raw_rfp, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 8:
        continue
    if int(line[5]) != 0:
        counter_rfp += 1

print (counter_gfp, counter_rfp)