import sys
sys.path.append("../")

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths
from Whole_Movie_Check_Plots.Tracking_CellID_Relabelling import VisualiseCellIDRelabelling

_, txt_file_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")

for file in txt_file_list:
    file = file.replace("raw", "sorted")
    print ("Processing filtered file: {}".format(file))
    odd_frames = VisualiseCellIDRelabelling(txt_file=file, show=True)
    print("Odd frames: {}".format(odd_frames))
