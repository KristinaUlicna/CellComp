import os
import sys
sys.path.append("../")

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths

def FindMovieLength(data_date):
    """ Returns movie_frames (integer) of how long the movie is
        according to the data_date argument (string). """

    movies = []     # = list of lists of absolute paths
    experiment_types = ["MDCK_WT_Pure", "MDCK_Sc_Tet-_Pure", "MDCK_Sc_Tet+_Pure", "MDCK_90WT_10Sc_NoComp"]
    for exp_type in experiment_types:
        xml_file_list, _ = GetMovieFilesPaths(exp_type=exp_type)
        movies.append(xml_file_list)

    for exp_type in movies:
        for file in exp_type:
            if data_date in file:
                directory = file.split("/")[:-2]
                directory = "/".join(directory) + "/segmented/"
                directory = os.listdir(directory)
                directory = [item for item in sorted(directory) if item.startswith("s_") and item.endswith(".tif")]
                return len(directory)
