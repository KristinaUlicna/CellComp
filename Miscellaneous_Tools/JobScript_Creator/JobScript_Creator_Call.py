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
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths

# Track all of your MDCK movies:
"""
movies = Get_MDCK_Movies_Paths()

for movie in movies:
    data_date, pos_number = movie.split("/")[-3], movie.split("/")[-2].split("pos")[-1]
    print (data_date, pos_number)
    call_template = ProcessMovies(pos=pos_number, data_date=data_date, exp_type="Cells_MDCK", user="Kristina")
    call_template.Tracking(to_track_GFP=True, to_track_RFP=False, timeout_seconds=3600)
"""

call_template = ProcessMovies(pos=0, data_date="extra", exp_type="Cells_MDCK", user="Kristina")
#call_template.SegClass_Old(BF=True, GFP=False, RFP=True)
call_template.Tracking(to_track_GFP=False, to_track_RFP=True, timeout_seconds=3600)
