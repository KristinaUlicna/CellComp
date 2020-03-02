import json
import os

def Shortlist_NonRoot_NonLeaf_Cells(directory):
    """

    :param directory:       .../tracks_XFP/ absolute directory with extracted json files per each track
    :return:
    """

    dividers_GFP = []
    dividers_RFP = []

    for f in os.listdir(directory):
        file = directory + f
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            if data['parent'] != 0 and data['fate'] == "DIVIDE":
                number = f.split("track_")[1]
                if "GFP" in number:
                    dividers_GFP.append(int(number.split("_GFP.json")[0]))
                if "RFP" in number:
                    dividers_RFP.append(int(number.split("_RFP.json")[0]))
    return sorted(dividers_GFP), sorted(dividers_RFP)


directory = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_RFP/"
dividers_GFP, dividers_RFP = Shortlist_NonRoot_NonLeaf_Cells(directory=directory)
print ("GFP Dividers: len = {}; {}".format(len(dividers_GFP), dividers_GFP))
print ("RFP Dividers: len = {}; {}".format(len(dividers_RFP), dividers_RFP))
