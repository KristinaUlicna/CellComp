# TODO: Print cells with longer than 20hrs division time:

file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
       "tracks_try_55/analysis/channel_RFP/cellIDdetails_raw.txt"

for line in open(file, "r"):
    line = line.rstrip().split("\t")
    if line[0] != "Cell_ID" and len(line) == 8:
        if float(line[4]) >= 20.0:
            if line[6] == "False" and line[7] == "False":
                print (line)

"""
# tracks_try_56:
['552', '715', '1077', '1448', '24.13', '3', 'False', 'False']
['572', '728', '1093', '1460', '24.33', '2', 'False', 'False']
['143', '217', '727', '2040', '34.0', '1', 'False', 'False']
['59', '75', '567', '1968', '32.8', '1', 'False', 'False']
['582', '736', '1052', '1264', '21.07', '2', 'False', 'False']
['594', '744', '1064', '1280', '21.33', '1', 'False', 'False']
['524', '700', '1064', '1456', '24.27', '1', 'False', 'False']
['330', '499', '981', '1928', '32.13', '2', 'False', 'False']
['614', '766', '1101', '1340', '22.33', '1', 'False', 'False']

# tracks_try_55:
['606', '715', '1018', '1212', '20.2', '3', 'False', 'False']
['605', '715', '1077', '1448', '24.13', '3', 'False', 'False']
['576', '700', '1064', '1456', '24.27', '3', 'False', 'False']
['625', '728', '1093', '1460', '24.33', '3', 'False', 'False']
['674', '766', '1101', '1340', '22.33', '3', 'False', 'False']
['621', '726', '1054', '1312', '21.87', '1', 'False', 'False']
['448', '593', '1042', '1796', '29.93', '1', 'False', 'False']
['616', '723', '1032', '1236', '20.6', '1', 'False', 'False']
['652', '744', '1064', '1280', '21.33', '1', 'False', 'False']

"""