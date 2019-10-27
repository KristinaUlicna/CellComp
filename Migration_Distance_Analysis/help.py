from Cell_Cycle_Duration.Find_Family_Class import FindFamily
from Cell_IDs_Analysis.Plotter_Lineage_Trees import PlotLineageTree
"""
merged_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"
call = FindFamily(cell_ID="1361-pos7-17_01_24", filtered_file=merged_file)
root = call.FindRoot()
"""
#print (root)
xml = '/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_01_24/pos7/tracks/tracks_type1.xml'
PlotLineageTree(root_ID=1076, xml_file=xml, show=True)
