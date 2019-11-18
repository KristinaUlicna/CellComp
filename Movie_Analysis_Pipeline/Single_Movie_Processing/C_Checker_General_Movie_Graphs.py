# # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                 #
# ----- Plotter of Movie Graphical Checks   ----- #
#                                                 #
# ----- Creator :           Kristina ULICNA ----- #
#                                                 #
# ----- Last Updated :        20th Sep 2019 ----- #
#                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # #


# Import all the necessary libraries:
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import statistics as stats
import numpy as np
import math
import os
import sys
sys.path.append("../")
from Whole_Movie_Check_Plots.Movie_Frame_Length import FindMovieLength


class AnalyseAllCellIDs(object):
    """
    lifetime
    cellcount per frame
    abs time vs cct
    hist cct
    relabelling
    """

    def __init__(self, txt_file):
        """ Plots analysis graphs for each movie & distributes them into specific directories depending on the input file:

        Args:
            txt_file (string)   ->   absolute path to a 'cellIDdetails_XXX.txt' file.
                                     '_raw.txt'     ->   directory = /analysis/movies/raw/
                                     '_sorted.txt'  ->   directory = /analysis/movies/trimmed/
        Return:
            None.
            Figures saved into appropriate directory.

        """

        directory = txt_file.split("/")[:-1]
        user, exp_type, data_date, pos = directory[-6], directory[-5], directory[-4], directory[-3]
        self.channel = directory[-2].split("channel_")[-1]
        #self.frames = FindMovieLength(exp_type=exp_type, data_date=data_date, pos=pos)
        self.frames = 1105
        self.directory = '/'.join(directory) + "/"

        if "raw" in txt_file:
            self.raw_file = txt_file
            self.filtered_file = txt_file.replace("raw", "filtered")
        if "filtered" in txt_file:
            self.raw_file = txt_file.replace("filtered", "raw")
            self.filtered_file = txt_file

        # Values to be calculated:
        self.median = None
        self.mean = None
        self.std = None


    def PlotCellIDLifeTime(self, show=False):
        """ Read the .txt file with cell_ID details to plot the length of each cell_id's life (in frames).
            Multiple dot-like life times indicate cell_IDs which appear for a limited number of frames.
        """

        # Prepare the axes:
        cell_ID_label_list = []
        cell_ID_frame_list = []

        for line in open(self.raw_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8 or line[0] == '':
                continue
            cell_ID_label_list.append([int(line[0]), int(line[0])])
            cell_ID_frame_list.append([int(line[1]), int(line[2])])  # includes the last frame

        # Plot the thing:
        for x, y in zip(cell_ID_frame_list, cell_ID_label_list):
            plt.plot(x, y)
        plt.xticks(np.arange(0, self.frames + 201, step=200))
        plt.xlim(-50, self.frames + 50)
        plt.xlabel('Frame number')
        plt.ylabel('Cell ID label')
        plt.title('Lifetime of {} cell_ID labels\n(movie = {} frames)'.format(self.channel, self.frames))

        # Save, show & close:
        plt.savefig(self.directory + "Plot_CellIDLabel_LifeTime.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotCellIDsPerFrame(self, show=False, trimming_limit=75):
        """ Read the .txt file with cell_ID details to plot cell count per each frame.
            Cell count should increase linearly or exponentially (ideal conditions).
        """

        # My txt_files count frames from 0, not from 1 (python-style):
        frame_cell_count_raw = [0 for _ in range(self.frames)]
        frame_cell_count_real = [0 for _ in range(self.frames)]
        frame_cell_count_filt = [0 for _ in range(self.frames)]
        trimming_limit = trimming_limit * 4 / 60

        for line in open(self.raw_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8 or line[0] == '':
                continue
            fr_st, fr_en = int(line[1]), int(line[2])

            # Include all cells in 'raw':
            for index in range(fr_st, fr_en + 1):
                frame_cell_count_raw[index] += 1

            # Include only over 5hrs and non-root/non-leaf cells in 'filtered':
            if float(line[4]) > float(trimming_limit):
                if line[6] == "False" and line[7] == "False":
                    for index in range(fr_st, fr_en + 1):
                        frame_cell_count_real[index] += 1

            # START Special case: Include cells that are non-leaf but have short lifetime due to quick doubling:
            if float(line[4]) <= float(trimming_limit) and fr_st == 0:
                if line[6] == "True" and line[7] == "False":
                    for index in range(fr_st, fr_en + 1):
                        frame_cell_count_real[index] += 1

            # END Special case: Include cells that are non-root but have short lifetime due to end of imaging:
            if float(line[4]) <= float(trimming_limit) and fr_en == self.frames - 1 or fr_en == self.frames - 2:
                if line[6] == "False" and line[7] == "True":
                    for index in range(fr_st, fr_en + 1):
                        frame_cell_count_real[index] += 1

        # For comparison, process the 'cellIDdetails_filtered.txt' (should give the same curve except for the )
        for line in open(self.filtered_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8 or line[0] == '':
                continue
            fr_st, fr_en = int(line[1]), int(line[2])
            for index in range(fr_st, fr_en + 1):
                frame_cell_count_filt[index] += 1

        # Plot the thing:
        x_axis = list(range(0, self.frames, 1))
        plt.scatter(x_axis, frame_cell_count_raw, c="salmon", alpha=0.5, label="From 'cellIDdetails_raw.txt' - all cells")
        plt.scatter(x_axis, frame_cell_count_real, c="gold", alpha=0.5, label="From 'cellIDdetails_raw.txt' - compensated for start/end cells")
        plt.scatter(x_axis, frame_cell_count_filt, c="plum", alpha=0.5, label="From 'cellIDdetails_filtered.txt' - only non-root/non-leaf cells")
        plt.xlim(-100, self.frames + 100)
        plt.xticks(np.arange(0, self.frames + 201, step=200))
        plt.xlabel('Frame number')
        plt.ylabel('Cell count (total cell_IDs)')
        plt.title('Cell_ID Labels Count ({}) per Frame\n(movie = {} frames)'.format(self.channel, self.frames))
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)

        # Save, show & close:
        plt.savefig(self.directory + "Plot_CellIDCount_PerFrame.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotCellCycleAbsTime(self, show=False):
        """ Read the sorted .txt file with cell_ID details to plot graphs. """

        x_axis_raw = []
        y_axis_raw = []
        for line in open(self.raw_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8 or line[0] == '':
                continue
            x_axis_raw.append(int(line[1]) * 4)
            y_axis_raw.append(int(line[3]))

        x_axis_fil = []
        y_axis_fil = []
        for line in open(self.filtered_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8 or line[0] == '':
                continue
            x_axis_fil.append(int(line[1]) * 4)
            y_axis_fil.append(int(line[3]))

        ticks = list(range(0, self.frames * 4 + 401, 400))
        plt.scatter(x_axis_raw, y_axis_raw, alpha=0.3, c="gold", label="From 'cellIDdetails_raw.txt'")
        plt.scatter(x_axis_fil, y_axis_fil, alpha=0.3, c="forestgreen", label="From 'cellIDdetails_filtered.txt'")
        plt.plot([0, self.frames * 4], [self.frames * 4, 0], linewidth=1.2, linestyle='dashed', color='grey', alpha=0.7)
        plt.xlim(-200, self.frames * 4 + 200)
        plt.xticks(ticks, rotation='vertical')
        plt.xlabel("Absolute time [mins]")
        plt.ylim(-200, self.frames * 4 + 200)
        plt.yticks(ticks)
        plt.ylabel("Cell cycle time [mins]")
        plt.title("Absolute time vs Cell cycle duration of {} cell_IDs\n(movie = {} frames)".format(self.channel, self.frames))
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)

        # Save, show & close:
        plt.savefig(self.directory + "Scatter_AbsTime_vs_CCT.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotHistCellCycleTime(self, show=False):
        """ Args:   Limit   -> (integer; set to 80 by default)  =  whole time of the movie in hours. """

        # Extract cell cycle duration according to given limit:
        cct_hrs = []
        for line in open(self.filtered_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8 or line[0] == '':
                continue
            cct_hrs.append(float(line[4]))

        # Define bin edges & set axes ticks according to the limit:
        ticks_hrs = list(range(0, 81, 10))
        bin_edges = list(range(0, 81, 4))

        # Calculate the mean & standard deviations:
        if len(cct_hrs) <= 2:
            self.mean, self.std = 0, 0
        else:
            self.mean = round(stats.mean(cct_hrs), 2)
            self.std = round(stats.stdev(cct_hrs), 2)

        # Plot the thing: < B I G  P L O T >
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.2)

        ax1 = fig.add_subplot(111)
        n_per_bin, _, _ = ax1.hist(cct_hrs, bins=bin_edges, color='royalblue', edgecolor='royalblue', linewidth=1.2, alpha=0.5)
        ax1.set_title("Cell Cycle Duration of {} Cell_IDs\nmean ± st.dev = {} ± {} (movie = {} frames)"
                      .format(self.channel, self.mean, self.std, self.frames))

        # Y-axis: Find y-axis maximum to define lower limit of y-axis
        ax1.set_ylabel("Cell ID count")
        ax1.set_ylim((n_per_bin.max() * -1) / 10)       # y_lim = -10% of max y-axis value
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

        # X-axis: Hour scale:
        ax1.set_xlim(ticks_hrs[0] - 4, ticks_hrs[-1] + 4)
        ax1.set_xticks(ticks_hrs)
        ax1.set_xlabel("Cell Cycle Time [hours]")

        # Plot the thing: < S U B  P L O T >
        start, end = 10, 30
        bins_interval = list(range(start, end + 1, 1))
        cct_hrs_interval = [item for item in cct_hrs if float(item) > start and float(item) < end]

        sub_axes = plt.axes([0.45, 0.5, 0.4, 0.35])  # left, bottom, width, height
        n_per_bin_interval, _, _ = sub_axes.hist(x=cct_hrs_interval, bins=bins_interval, color='lightgreen',
                                                 alpha=0.8, edgecolor='green', linewidth=1.0)
        upper = int(max(n_per_bin_interval))
        if upper <= 20:
            step_size = 2
        else:
            step_size = 5
        sub_axes.set_xticks(list(range(start, end + 1, 2)))
        sub_axes.set_yticks(list(range(0, upper + step_size, step_size)))
        sub_axes.set_ylim(-1.0, upper + step_size)

        sub_axes.axvline(self.mean, color='gold', linestyle='dashed', linewidth=1.5, label="Mean Gen #1")
        sub_axes.axvline(self.mean + self.std, color='gold', linestyle='dashed', linewidth=1.0)
        sub_axes.axvline(self.mean - self.std, color='gold', linestyle='dashed', linewidth=1.0)

        # Save, show & close:
        plt.savefig(self.directory + "Hist_Cell_Cycle_Duration.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotCellIDRelabelling(self, show=False, print_stats=False):
        """ Plot the barplot for each 'cellIDdetails_sorted.txt' (or '_raw.txt') file
            to see how many cellIDs get re-labelled at each frame.

        Args:
            txt_file (string)       -> absolute directory to 'cellIDdetails_sorted.txt'

        Return:
            None.
            Visualises a figure & saves it in specified directory.

        """

        frame_appear = []
        frame_ceased = []

        for line in open(self.raw_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or len(line) < 8 or line[0] == '':
                continue
            # Aim for Root & Leaf cells only:
            if line[6] == "True" and line[7] == "True":
                frame_appear.append(int(line[1]))
                frame_ceased.append(int(line[2]))

        # Count how many times each frame is mentioned in the created lists:
        frame_list = list(range(0, self.frames, 1))
        axis_frames = [item + 1 for item in frame_list]
        axis_frames.pop(-2)
        axis_appear = []
        axis_ceased = []

        for frame in frame_list:
            axis_appear.append(frame_appear.count(frame))
            axis_ceased.append(frame_ceased.count(frame))

        # Modify 'axis_appear' list to shift it one item to the left relative to 'axis-cease' list:
        cells_start = axis_appear.pop(0)    # remove the starting count of cells
        axis_appear = axis_appear + [0]     # add 0 to the end to even the lengths of the axes lists

        # Pop the last 2 frames out:
        axis_appear.pop(-1)
        axis_appear.pop(-1)
        axis_ceased.pop(-1)
        axis_ceased.pop(-1)

        if print_stats is True:
            print ("Seeded cells: cell count at the 1st frame: {}".format(cells_start))
            print ("X-Axis: len = {}\t{}".format(len(axis_frames), axis_frames))
            print ("Y-Axis Appear: len = {}\t{}".format(len(axis_appear), axis_appear))
            print ("Y-Axis Ceased: len = {}\t{}".format(len(axis_ceased), axis_ceased))

        # Create return vector to check for odd frames where a lot of re-labelling happens:
        odd_frames = []
        cut_off = 20
        for index, (i, j) in enumerate(zip(axis_appear, axis_ceased)):
            if i > cut_off or j > cut_off:
                odd_frames.append(index + 1)

        # Do these odd frames come in pairs?
        odd_pairs = 0
        current_frame = 0
        for number in odd_frames:
            if number == current_frame + 1:
                odd_pairs += 1
            current_frame = number

        if print_stats is True:
            percentage = round(float(odd_pairs) / (len(odd_frames) / 2) * 100, 2)
            print ("{}% of odd frames (where over {} cellIDs are re-labelled) come in pairs.".format(percentage, cut_off))


        # Plot the thing:

            # Full-sized figure:
        plt.figure(figsize=(18, 6))
        plt.bar(x=np.array(axis_frames)-0.2, height=axis_ceased, width=0.4, color="green", label="Cells ceasing at frame 'n'")
        plt.bar(x=np.array(axis_frames)+0.2, height=axis_appear, width=0.4, color="orange", label="Cells appearing at frame 'n+1'")
        plt.title("CellID 're-labelling' issue by the tracker (v0.2.9)"
                  "\n{} Root & Leaf cellIDs only included; {} seeded cells at 1st frame".format(len(frame_ceased), cells_start))

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)      # bbox_to_anchor (tuple) -> (x-axis, y-axis)
        plt.xlim(-10, 1210)
        plt.ylim(-5, 150)
        plt.grid(b=None, which='major', axis='y')
        plt.ylabel("Count of cell-IDs ceasing/appearing")
        yticks = list(range(0, 146, 10))
        plt.yticks(ticks=yticks, labels=yticks)
        #plt.yticks(list(range(0, 111, 10)))
        plt.xlabel("Frame number")
        xticks = list(range(0, movie_length + 200, 200))
        plt.xticks(ticks=xticks, labels=xticks)

            # Detailed figure:
        start, end = 0, 20
        sub_axes = plt.axes([0.17, 0.4, 0.5, 0.45])       # left, bottom, width, height
        sub_axes.bar(x=np.array(axis_frames[start:end])-0.2, height=axis_ceased[start:end], width=0.4, color="green")
        sub_axes.bar(x=np.array(axis_frames[start:end])+0.2, height=axis_appear[start:end], width=0.4, color="orange")
        sub_axes.grid(b=None, which='major', axis='y')
        sub_axes.set_xticks(np.array(range(start + 1, end + 1)))
        sub_axes.set_ylim(-0.2)

            # Save, show & close:
        plt.savefig(self.directory + "CellID_Relabelling.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()

        return odd_frames