# TODO: Plot cumulative histogram that will show:
# predicted distribution (thick black line)
# & all individual movies (thinner lines);
# "MDCK_WT_Pure" = 18 movies


import sys
sys.path.append("../")
from Cell_Cycle_Duration.Cumul_Hist_All_Movies_Function import PlotHistCumul_AllMovies


# Call the function:
for gen in [1, 2, 3]:
    PlotHistCumul_AllMovies(exp_type="MDCK_WT_Pure", generation=gen, show=True)