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
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_HeLa_Movies_Paths

# Track all of your MDCK movies:

#movies = Get_HeLa_Movies_Paths()

for pos in [0, 2, 4, 6, 8, 10]:
    call_template = ProcessMovies(pos=pos, data_date="17_03_27", exp_type="MDCK_90WT_10Sc_NoComp", user="Kristina")
    #call_template.SegClass_Old(BF=True, GFP=True, RFP=True)
    call_template.Tracking(to_track_GFP=True, to_track_RFP=True)

for pos in [0, 2, 4, 9, 11, 13]:
    call_template = ProcessMovies(pos=pos, data_date="17_07_24", exp_type="MDCK_90WT_10Sc_NoComp", user="Kristina")
    #call_template.SegClass_Old(BF=True, GFP=True, RFP=True)
    call_template.Tracking(to_track_GFP=True, to_track_RFP=True)

