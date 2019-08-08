#TODO: Script to call the extractor class

import sys
sys.path.append("../")

# Extract info to produce 'cellIDdetails_raw.txt':
from Cell_IDs_Analysis.Extractor_CellIDdetails_Class import GetCellDetails
"""
xml_file_type1 = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_type1.xml"
xml_file_type2 = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_type2.xml"

GetCellDetails(xml_file=xml_file_type1).IterateTrees()
GetCellDetails(xml_file=xml_file_type2).IterateTrees()
"""

# Process the 'cellIDdetails_raw.txt' file:
from Whole_Movie_Check_Plots.Process_Raw_TxtFile import ProcessRawTxtFile

raw_file_GFP = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/analysis/channel_GFP/cellIDdetails_raw.txt"
raw_file_RFP = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/analysis/channel_RFP/cellIDdetails_raw.txt"

call = ProcessRawTxtFile(raw_file=raw_file_GFP)
call.TrimCellIDFile()
call.SortCellIDFile()
call.FilterCellIDFile()

call = ProcessRawTxtFile(raw_file=raw_file_RFP)
call.TrimCellIDFile()
call.SortCellIDFile()
call.FilterCellIDFile()
