# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
# ----- Job Script Creator for SegClass & Tracking Jobs ----- #
#                                                             #
# ----- Creator :           Kristina ULICNA             ----- #
#                                                             #
# ----- Last updated :      13th May 2019               ----- #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Call the class 'ProcessMovies' & its 'SegClass' & 'Tracking' functions:
from Miscellaneous_Tools.JobScript_Creator.JobScript_Creator_Class import ProcessMovies
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import GetMovieFilesPaths

# Track your template movie:
for pos in [7, 8, 9]:
    call_template = ProcessMovies(pos=pos, data_date='17_01_24', exp_type="MDCK_WT_Pure", user="Kristina")
    call_template.Tracking(to_track_GFP=True, to_track_RFP=False)

# Loop through models:
"""
call_template = ProcessMovies(pos=13, data_date='17_07_24', exp_type="MDCK_90WT_10Sc_NoComp", user="Kristina")
for number in [56]:
    call_template.SegClass(BF=True, GFP=True, RFP=True, ResNet=True)
    #call_template.Tracking(to_track_GFP=True, to_track_RFP=True, config_number=number, timeout_seconds=1800)
"""
"""
maxi_file_list = []

for exp_type in ["MDCK_WT_Pure", "MDCK_Sc_Tet-_Pure", "MDCK_90WT_10Sc_NoComp"]:
    call = GetMovieFilesPaths(exp_type=exp_type)
    xml_file_list = call.GetChannelXmlFiles()
    for xml_file in xml_file_list:
        maxi_file_list.append(xml_file)


counter = 0
for file in maxi_file_list:

    file = file.split("/")
    exp_type, data_date, pos = file[-5], file[-4], file[-3].split("pos")[-1]
    call_template = ProcessMovies(pos=pos, data_date=data_date, exp_type=exp_type, user="Kristina")
    if not "Pure" in exp_type:
        call_template.SegClass(BF=True, GFP=True, RFP=True, ResNet=True)
    else:
        if "WT" in exp_type:
            call_template.SegClass(BF=True, GFP=True, RFP=False, ResNet=True)
        elif "Sc" in exp_type:
            call_template.SegClass(BF=True, GFP=False, RFP=True, ResNet=True)

    counter += 1
    #call_template.Tracking(to_track_GFP=True, to_track_RFP=False)


print (counter)
print (counter == len(maxi_file_list))
"""