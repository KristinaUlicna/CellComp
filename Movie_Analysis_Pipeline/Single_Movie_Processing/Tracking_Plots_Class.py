# # # # # # # # # # # # # # # # # # # # # # # # #
#                                               #
# ----- All Tracked CellID Info Analysis  ----- #
#                                               #
# ----- Creator :        Kristina ULICNA  ----- #
#                                               #
# ----- Last updated :   17th May 2019    ----- #
#                                               #
# # # # # # # # # # # # # # # # # # # # # # # # #


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

        exp_type = txt_file.split("/")[-5]
        data_date = txt_file.split("/")[-4]
        position = txt_file.split("/")[-3]
        if "channel_" in txt_file:
            exp_type = txt_file.split("/")[-6]
            data_date = txt_file.split("/")[-5]
            position = txt_file.split("/")[-4]
        frames = FindMovieLength(exp_type=exp_type, data_date=data_date, pos=position)
        data_type = None

        directory = txt_file.split("/")[:-1]
        directory = '/'.join(directory) + "/"
        if "raw" in txt_file:
            directory += "/movie/raw/"
            data_type = "raw"
        if "sorted" in txt_file or "filtered" in txt_file:
            directory += "/movie/trimmed/"
            data_type = "trimmed"
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.directory = directory
        self.txt_file = txt_file
        self.frames = frames
        self.data_type = data_type

        self.mean = None
        self.std = None


    def PlotCellIDLifeTime(self, show=False):
        """ Read the .txt file with cell_ID details to plot the length of each cell_id's life (in frames).
            Multiple dot-like life times indicate cell_IDs which appear for a limited number of frames.
        """

        # Prepare the axes:
        cell_ID_label_list = []
        cell_ID_frame_list = []

        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8:
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
        plt.title('Lifetime of {} cell_ID labels\n(movie = {} frames)'.format(self.data_type, self.frames))

        # Save, show & close:
        plt.savefig(self.directory + "Plot_CellIDLabel_LifeTime.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotCellIDsPerFrame(self, show=False):
        """ Read the .txt file with cell_ID details to plot cell count per each frame.
            Cell count should increase linearly or exponentially (ideal conditions).
        """

        # My txt_files count frames from 0, not from 1 (python-style):
        frame_cell_count = [0 for _ in range(self.frames)]

        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8:
                continue
            fr_st, fr_en = int(line[1]), int(line[2])
            for index in range(fr_st, fr_en + 1):
                frame_cell_count[index] += 1

        x_axis = np.arange(0, self.frames, 1)
        y_axis = np.array(frame_cell_count)

        # Plot the thing:
        plt.scatter(x_axis, y_axis, c="salmon", alpha=0.5)
        plt.xlim(-100, self.frames + 100)
        plt.xticks(np.arange(0, self.frames + 201, step=200))
        plt.xlabel('Frame number')
        plt.ylabel('Cell count (total cell_IDs)')
        plt.title('Cell_ID Labels Count ({}) per Frame\n(movie = {} frames)'.format(self.data_type, self.frames))

        # Save, show & close:
        plt.savefig(self.directory + "Plot_CellIDCount_PerFrame.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotCellCycleAbsoluteTime(self, show=False):
        """ Read the sorted .txt file with cell_ID details to plot graphs. """

        x_axis = []
        y_axis = []
        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8:
                continue
            x_axis.append(int(line[1]) * 4)
            y_axis.append(int(line[3]))

        ticks = list(range(0, self.frames * 4 + 401, 400))
        plt.scatter(x_axis, y_axis, alpha=0.3, c="forestgreen")
        plt.plot([0, self.frames * 4], [self.frames * 4, 0], linewidth=1.2, linestyle='dashed', color='grey', alpha=0.7)
        plt.xlim(-200, self.frames * 4 + 200)
        plt.xticks(ticks, rotation='vertical')
        plt.xlabel("Absolute time [mins]")
        plt.ylim(-200, self.frames * 4 + 200)
        plt.yticks(ticks)
        plt.ylabel("Cell cycle time [mins]")
        plt.title("Absolute time vs Cell cycle duration of {} cell_IDs\n(movie = {} frames)".format(self.data_type, self.frames))

        # Save, show & close:
        plt.savefig(self.directory + "Scatter_AbsTime_vs_CCT.png", bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotHistCellCycleDurationORIGINAL(self, limit=80, show=False):
        """ Args:   Limit   -> (integer; set to 80 by default)  =  whole time of the movie in hours. """

        if int(limit) > 80:
            raise Exception("Warning, limit of {} is out of range of the movie duration (max. 80 hrs)".format(str(limit)))

        # Extract cell cycle duration according to given limit:
        cct_hrs = []
        for line in open(self.txt_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8:
                continue
            # Include only non-root & non-leaf cell_IDs:
            if line[6] == "False" and line[7] == "False":
                if float(line[4]) <= float(limit):
                    cct_hrs.append(float(line[4]))

        # Define bin edges & set axes ticks according to the limit:
        if limit > 5:
            ticks_hrs = list(range(0, int(limit) + 1, int(int(limit) / 10)))
            ticks_min = [int(tick) * 60 for tick in ticks_hrs]
            bin_edges = list(range(0, limit + 1, int(limit / 20)))
        else:
            ticks_hrs = list(range(0, int(limit) + 1))
            ticks_min = [int(tick) * 60 for tick in ticks_hrs]
            ticks_min = list(range(ticks_min[0], ticks_min[-1] + 1, 20))
            bin_edges = list(range(0, limit * 60 + 1, int(limit * 60 / 15)))
            bin_edges = [item / 60 for item in bin_edges]


        # Calculate the mean & standard deviations:
        if len(cct_hrs) <= 2:
            mean, std = 0, 0
        else:
            mean = round(stats.mean(cct_hrs), 2)
            std = round(stats.stdev(cct_hrs), 2)

        # Plot the thing: < B I G  P L O T >
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.2)

        ax1 = fig.add_subplot(111)
        n_per_bin, _, _ = ax1.hist(cct_hrs, bins=bin_edges, color='lightskyblue', edgecolor='royalblue', linewidth=1.2)
        ax1.set_title("Cell Cycle Duration of {} Cell_IDs\nmean ± st.dev = {} ± {} (movie = {} frames)"
                      .format(self.data_type, mean, std, self.frames))

        # Y-axis: Find y-axis maximum to define lower limit of y-axis
        ax1.set_ylabel("Cell ID count")
        ax1.set_ylim((n_per_bin.max() * -1) / 10)       # y_lim = -10% of max y-axis value
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

        # X-axis: Hour scale:
        tick_limit = limit / 20
        ax1.set_xlim(ticks_hrs[0] - tick_limit, ticks_hrs[-1] + tick_limit)
        ax1.set_xticks(ticks_hrs)
        ax1.set_xlabel("Cell Cycle Time [hours]")

        # X-axis: Minute scale:
        ax2 = ax1.twiny()
        ax2.set_xlim(ticks_min[0] - tick_limit * 60, ticks_min[-1] + tick_limit * 60)
        ax2.set_xticks(ticks_min)
        ax2.set_xlabel("Cell Cycle Time [mins]")

        # Move twinned axis ticks and label from top to bottom & offset the twin axis below the host:
        ax2.xaxis.set_ticks_position("bottom")
        ax2.xaxis.set_label_position("bottom")
        ax2.spines["bottom"].set_position(("axes", -0.15))


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

        sub_axes.axvline(mean, color='gold', linestyle='dashed', linewidth=1.5, label="Mean Gen #1")
        sub_axes.axvline(mean + std, color='gold', linestyle='dashed', linewidth=1.0)
        sub_axes.axvline(mean - std, color='gold', linestyle='dashed', linewidth=1.0)

        # Save, show & close:
        plt.savefig(self.directory + "Hist_Cell_Cycle_Duration.png".format(limit), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotHistCellCycleDuration(self, show=False):
        """ Args:   Limit   -> (integer; set to 80 by default)  =  whole time of the movie in hours. """

        # Extract cell cycle duration according to given limit:
        cct_hrs = []
        for line in open(self.txt_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID' or len(line) < 8:
                continue
            # Include only non-root & non-leaf cell_IDs:
            if line[6] == "False" and line[7] == "False":
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
                      .format(self.data_type, self.mean, self.std, self.frames))

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


call = AnalyseAllCellIDs(txt_file="/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/analysis/channel_RFP/cellIDdetails_trimmed.txt")
call.PlotCellIDsPerFrame(show=True)
call.PlotCellIDLifeTime(show=True)