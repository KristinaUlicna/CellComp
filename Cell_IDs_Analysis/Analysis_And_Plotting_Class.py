# # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                 #
# ----- Tracked CellID Information Analysis ----- #
#                                                 #
# ----- Creator :     Kristina ULICNA       ----- #
#                                                 #
# ----- Date :        10th May 2019         ----- #
#                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # #


# Import all the necessary libraries:
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np

class AnalyseCellIDs():

    def __init__(self, txt_file):

        self.txt_file = txt_file
        directory = str(self.txt_file).split("/")
        directory = directory[:-1]
        self.directory = '/'.join(directory) + "/"


    def SortCellIDFile(self):
        """ Sorts the file by the first column -> int(line[0]) <- in numerical order by overwriting the file.
            Args:       Insert the file name (end with .txt) with absolute directory.
            Details:    ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]."""

        # Read the txt_file & divide into header & lines to be sorted:
        header_list = []
        line_list = []
        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID':
                header_list = line
            else:
                try:
                    line[0] = int(line[0])
                except:
                    continue
                line_list.append(line)

        # Re-write the file & type the header:
        file = open(self.txt_file, 'w')
        header_string = ''
        for item in header_list:
            header_string += item + "\t"
        header_string = header_string[:-1]
        header_string += "\n"
        file.write(header_string)

        # Sort the lines numerically according to the cell_ID, write & close:
        for line in sorted(line_list, key=itemgetter(0)):
            string = ''
            for item in line:
                string += str(item) + "\t"
            string = string[:-1]
            string += "\n"
            file.write(string)
        file.close()


    def PlotCellIDLifeTime(self):
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
        plt.xlabel('Frame number')
        plt.ylabel('Cell ID label')
        plt.title('Lifetime of all cell_ID labels')
        plt.savefig(self.directory + "Plot_Cell_ID_Label_LifeTime.jpeg", bbox_inches="tight")
        plt.show()
        plt.close()


    def PlotCellIDsPerFrame(self):
        """ Read the sorted .txt file with cell_ID details to plot graphs. """

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
        plt.xticks(np.arange(0, 1200 + 1, step=300))
        plt.xlabel('Frame number')
        plt.ylabel('Cell count (total cell_IDs)')
        plt.title('Cell Count per Frame (Count of Cell_ID Labels)')
        plt.savefig(self.directory + "Plot_Cell_ID_Count_Per_Frame.jpeg", bbox_inches="tight")
        plt.show()
        plt.close()


    def PlotCellCycleAbsoluteTime(self):
        """ Read the sorted .txt file with cell_ID details to plot graphs. """

        x_axis_3 = []
        y_axis_3 = []
        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == 'Cell_ID':
                continue
            x_axis_3.append(int(line[1]) * 4)
            y_axis_3.append(int(line[3]))
        #self.txt_file.close()

        plt.scatter(x_axis_3, y_axis_3, alpha=0.3)
        plt.xlim(-200, 5000)
        plt.xticks(list(range(0, 4801, 400)))
        plt.xlabel("Absolute time [mins]")
        plt.ylabel("Cell cycle time [mins]")
        plt.title("Absolute time vs Cell cycle duration")
        plt.savefig(self.directory + "Absolute_Time_per_Cell_Cycle_Time.jpeg", bbox_inches="tight")
        plt.show()
        plt.close()


    def PlotHist_CellCycleDuration(self, limit=80):
        """ Read the sorted .txt file with cell_ID details to plot graphs.
            Limit set to 80 by default = whole time of the movie in hours.
            Automatically incorporates
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


        # Set axes ticks according to the limit:
        if limit <= 2:
            ticks_hrs = list(range(0, int(limit) + 1))
        else:
            ticks_hrs = list(range(0, int(limit) + 1, int(int(limit)/10)))
        ticks_min = [int(tick) * 60 for tick in ticks_hrs]

        # Plot the thing:
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.2)
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()

        ax1.hist(cct_hrs)
        ax1.set_title("Cell Cycle Duration of Cell_IDs with division time below {} hours".format(limit))

        # Y-axis: Find y-axis maximum to define lower limit of y-axis
        y, _, _ = plt.hist(cct_hrs)
        ax1.set_ylim(int((y.max() * -1) / 10))      # y_lim = -10% of max y-axis value
        ax1.set_ylabel("Cell ID count")

        # X-axis: Hour scale:
        tick_limit = limit / 20
        ax1.set_xlim(ticks_hrs[0] - tick_limit, ticks_hrs[-1] + tick_limit)
        ax1.set_xticks(ticks_hrs)
        ax1.set_xlabel("Cell Cycle Time [hours]")

        # X-axis: Minute scale:
        ax2.set_xlim(ticks_min[0] - tick_limit * 60, ticks_min[-1] + tick_limit * 60)
        ax2.set_xticks(ticks_min)
        ax2.set_xlabel("Cell Cycle Time [mins]")

        ax2.xaxis.set_ticks_position("bottom")
        ax2.xaxis.set_label_position("bottom")
        ax2.spines["bottom"].set_position(("axes", -0.15))

        # Save, show & close:
        plt.savefig(self.directory + "Hist_Cell_Cycle_Duration_{}hours.jpeg".format(limit), bbox_inches="tight")
        plt.show()
        plt.close()


# TODO: Remove those weird lines from the histogram
# TODO: Find out how to extract which cellIDs are plotted per each bin - explore what those are...
