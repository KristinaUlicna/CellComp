# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
# ----- Job Script Creator for SegClass & Tracking Jobs ----- #
#                                                             #
# ----- Creator :           Kristina ULICNA             ----- #
#                                                             #
# ----- Last updated :      13th May 2019               ----- #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
sys.path.append("../")

# Call the class 'ProcessMovies' & its 'SegClass' & 'Tracking' functions:
from JobScript_Creator.JobScriptCreator_Alan_Template_Class import ProcessMovies


# Track your template movie:
call_template = ProcessMovies(pos=13, data_date='17_07_24', exp_type="MDCK_90WT_10Sc_NoComp", user="Kristina")
call_template.Tracking(to_track_GFP=False, to_track_RFP=True, try_number=24)
