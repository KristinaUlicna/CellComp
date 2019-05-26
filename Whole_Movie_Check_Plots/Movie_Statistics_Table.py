import sys
sys.path.append("../")

from texttable import Texttable              # creates simple ASCII tables
from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths
from Whole_Movie_Check_Plots.Tracking_Plots_Class import AnalyseAllCellIDs


def GetMovieSummary(cell_type):
    """ Print a table & write a file summarising the properties of all movies available per experiment.
    Args:
        cell_type (string)  ->   Type of experiment.
                                 Options: "MDCK_WT_Pure", "MDCK_Sc_Tet-_Pure", "MDCK_Sc_Tet+_Pure"
    Return:
        None.
        Prints a table into a console.
        Writes a txt_file into the directory given by cell_type.
    """

    name = "C E L L  T Y P E : '{}'\n".format(cell_type)
    _, txt_file_list = GetMovieFilesPaths(exp_type=cell_type)

    movie_number = []
    movie_date = []
    movie_pos = []
    total_frames = []
    total_divisions = []
    mean_div_time = []
    std_div_time = []
    num_lines_sorted = []
    num_lines_filtered = []

    # How many movies do you have available?
    total_movies = 0
    if cell_type == "MDCK_WT_Pure":
        total_movies = 21
    if cell_type == "MDCK_Sc_Tet-_Pure":
        total_movies = 9
    if cell_type == "MDCK_Sc_Tet+_Pure":
        total_movies = 0


    for order, sorted_file in enumerate(sorted(txt_file_list)):
        sorted_file = sorted_file.replace("raw", "sorted")
        print ("Sorted File: {}".format(sorted_file))
        movie_number.append(order+1)
        movie_date.append(sorted_file.split("/")[-3])
        movie_pos.append(sorted_file.split("/")[-4])

        # Get empty frames:
        # TODO: An elegant way to find how many frames the movie has?
        x_axis, y_axis = AnalyseAllCellIDs(txt_file=sorted_file).PlotCellIDsPerFrame()
        for x, y in zip(x_axis, y_axis):
            if y == 0:
                total_frames.append(x-1)
                break

        # Get number of divisions (every non-leaf cell):
        div_counter = 0
        for line in open(sorted_file, 'r'):
            line = line.rstrip().split('\t')
            if line[0] == 'Cell_ID':
                continue
            if line[7] == "False":
                div_counter += 1
        total_divisions.append(div_counter)

        # Get mean division time per movie:
        # TODO: Should I exclude outliers?

        filtered_file = sorted_file.replace("sorted", "filtered")
        mean, std = AnalyseAllCellIDs(txt_file=filtered_file).PlotHist_CellCycleDuration(limit=80)
        mean_div_time.append(mean)
        std_div_time.append(std)

        # Count number of lines per file:
        num_lines_sorted.append(sum(1 for line in open(sorted_file))-1)
        num_lines_filtered.append(sum(1 for line in open(filtered_file))-1)

    # Write the table & file name & header:
    table = Texttable(max_width=0)
    print (name)
    header = ["Movie", "Date", "Pos", "Frames", "Divisions", "Mean Div Time", "St.Dev Div Time",
              "Lines-sorted.txt", "Lines-filtered.txt"]
    table.header(header)

    # Write into a new file:
    summary_file = "/Volumes/lowegrp/Data/Kristina/{}/summary_movies.txt".format(cell_type)
    summary_file = open(summary_file, "w")
    summary_file.write(name)
    header_string = ''
    for item in header:
        header_string += str(item) + "\t"
    header_string = header_string[:-1]
    header_string += "\n"
    summary_file.write(header_string)

    for i in list(range(0, total_movies)):
        my_list = [movie_number[i], movie_date[i], movie_pos[i], total_frames[i], total_divisions[i],
                   mean_div_time[i], std_div_time[i], num_lines_sorted[i], num_lines_filtered[i]]
        table.add_row(my_list)
        string = ''
        for item in my_list:
            string += str(item) + "\t"
        string = string[:-1]
        string += "\n"
        summary_file.write(string)

    # Print the table & close the newly-written file:
    print(table.draw())
    summary_file.close()


GetMovieSummary(cell_type="MDCK_WT_Pure")