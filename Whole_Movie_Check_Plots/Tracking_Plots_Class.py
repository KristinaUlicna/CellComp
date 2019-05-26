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


class AnalyseAllCellIDs(object):
    """ """

    def __init__(self, txt_file):
        """ Args:   txt_file (string)   ->   absolute path to a 'cellIDdetails_sorted.txt' file. """

        directory = txt_file.split("/")[:-1]
        directory = '/'.join(directory) + "/movie/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.directory = directory
        self.txt_file = txt_file


    def PlotCellIDLifeTime(self, show=False):
        """ Read the sorted .txt file with cell_ID details to plot graphs. """

        cell_ID_label_list = []
        cell_ID_frame_list = []

        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID':
                continue
            cell_ID_label_list.append(int(line[0]))
            cell_ID_frame_list.append(list(range(int(line[1]), int(line[2]) + 1)))  # includes the last frame
            if int(line[1]) > int(line[2]):
                raise Exception(
                    "Warning, frameAppears ({}) > frameDisappears ({}) ! Tracking error!".format(int(line[1]), int(line[2])))

        # Prepare the axes:
        x_axis = cell_ID_frame_list
        y_axis = []

        for cell_ID, frame_list in zip(cell_ID_label_list, cell_ID_frame_list):
            y_axis.append([cell_ID] * len(frame_list))

        # Plot the thing:
        for mini_x, mini_y in zip(x_axis, y_axis):
            plt.plot(mini_x, mini_y)
        plt.xticks(np.arange(0, 1200 + 1, step=200))
        plt.xlim(-50, 1250)
        plt.xlabel('Frame number')
        plt.ylabel('Cell ID label')
        plt.title('Lifetime of all cell_ID labels')
        plt.savefig(self.directory + "Plot_Cell_ID_Label_LifeTime.jpeg", bbox_inches="tight")

        if show is True:
            plt.show()
        plt.close()


    def PlotCellIDsPerFrame(self, show=False):
        """ Read the sorted .txt file with cell_ID details to plot graphs.

            # Output 2 lists:
        # cell_ID_frame_list -> [[0, 1, 2, ...], [0, 1, 2, ...], ...]
        # concat_frame_list -> [0, 1, 2, ..., 0, 1, 2, ..., ...] """

        cell_ID_frame_list = []

        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID':
                continue
            cell_ID_frame_list.append(list(range(int(line[1]), int(line[2]) + 1)))  # includes the last frame
            if int(line[1]) > int(line[2]):
                raise Exception(
                    "Warning, frameAppears ({}) > frameDisappears ({}) ! Tracking error!".format(int(line[1]), int(line[2])))

        # Prepare the axes:
        concat_frame_list = sum(cell_ID_frame_list, [])
        x_axis = list(range(1, 1200 + 1))
        y_axis = []

        for frame in x_axis:
            y_axis.append(concat_frame_list.count(frame))

        # Plot the thing:
        plt.scatter(x_axis, y_axis, c="salmon", alpha=0.5)
        plt.xlim(-100, 1300)
        plt.xticks(np.arange(0, 1200 + 1, step=200))
        plt.xlabel('Frame number')
        plt.ylabel('Cell count (total cell_IDs)')
        plt.title('Cell Count per Frame (Count of Cell_ID Labels)')
        plt.savefig(self.directory + "Plot_Cell_ID_Count_Per_Frame.jpeg", bbox_inches="tight")

        if show is True:
            plt.show()
        plt.close()

        return x_axis, y_axis
        # TODO: Plot an 'ideal' line into the graph?


    def PlotCellCycleAbsoluteTime(self, show=False):
        """ Read the sorted .txt file with cell_ID details to plot graphs. """

        x_axis_3 = []
        y_axis_3 = []
        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID':
                continue
            x_axis_3.append(int(line[1]) * 4)
            y_axis_3.append(int(line[3]))

        plt.scatter(x_axis_3, y_axis_3, alpha=0.3, c="forestgreen")
        plt.xlim(-200, 5000)
        plt.xticks(list(range(0, 4801, 400)))
        plt.xlabel("Absolute time [mins]")
        plt.ylim(-200, 5000)
        plt.yticks(list(range(0, 4801, 400)))
        plt.ylabel("Cell cycle time [mins]")
        plt.title("Absolute time vs Cell cycle duration")
        plt.savefig(self.directory + "Absolute_Time_per_Cell_Cycle_Time.jpeg", bbox_inches="tight")

        if show is True:
            plt.show()
        plt.close()


    def PlotHist_CellCycleDuration(self, limit=80, show=False):
        """ Read the sorted .txt file with cell_ID details to plot graphs.
        Args:
            Limit   -> (integer; set to 80 by default)      = whole time of the movie in hours.
        Return:
            n_per_bin, n_per_bin_length     = number of elements per each bin, number of bins

        """

        if int(limit) > 80:
            raise Exception("Warning, limit of {} is out of range of the movie duration (max. 80 hrs)".format(str(limit)))

        # Extract cell cycle duration according to given limit:
        cct_hrs = []
        for line in open(self.txt_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID':
                continue
            # Include only non-root & non-leaf cell_IDs:
            if line[6] == "False" and line[7] == "False":
                # Include only cell_IDs below the division time limit:
                if isinstance(limit, int):
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

        # Plot the thing:
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.2)

        ax1 = fig.add_subplot(111)
        n_per_bin, _, _ = ax1.hist(cct_hrs, bins=bin_edges, color='lightskyblue', edgecolor='royalblue', linewidth=1.2)
        ax1.set_title("Cell Cycle Duration of Cell_IDs with division time below {} hours".format(limit))

        # Visualise the mean & standard deviations:
        if len(cct_hrs) <= 2:
            mean, std = 0, 0
        else:
            mean = round(stats.mean(cct_hrs), 2)
            std = round(stats.stdev(cct_hrs), 2)

        ax1.axvline(mean, color='gold', linestyle='dashed', linewidth=1.5, label="Mean Gen #1")
        ax1.axvline(mean + std, color='gold', linestyle='dashed', linewidth=1.0)
        ax1.axvline(mean - std, color='gold', linestyle='dashed', linewidth=1.0)

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

        # Save, show & close:
        plt.savefig(self.directory + "Hist_Cell_Cycle_Duration_{}hours.jpeg".format(limit), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()

        return mean, std
