import matplotlib.pyplot as plt
import sys
sys.path.append("../")

from Movie_Analysis_Pipeline.Merging_Movie_Datasets.Find_Family_Class import FindFamily


def PlotJointProbabHistCCT(exp_type="MDCK_WT_Pure", show=False):
    """ Joint probability histograms with plt.hist2D on 'cellIDdetails_merged.txt' file.
        TASK: If you are a parent with certain cell cycle duration, what is your likelihood
                of producing progeny with the same cell cycle duration time?
    Args:
        exp_type (string)   -> "MDCK_WT_Pure" by default

    Return:
        None.
        Visualises the hist2D.
    """

    # Call FindFamily().FindParent() for each cell_ID to get real div.time of non-root parent & daughter - create 2 lists:
    merged_file = "/Volumes/lowegrp/Data/Kristina/{}/cellIDdetails_merged.txt".format(exp_type)
    x_axis_list = [[], [], []]
    y_axis_list = [[], [], []]

    for line in open(merged_file, 'r'):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or len(line) < 8:
            continue
        parent_info = FindFamily(cell_ID=line[0], filtered_file=merged_file).FindParent()
        if parent_info is not None and parent_info[1] != "NaN" and isinstance(parent_info[1], float):
            x_axis_list[parent_info[2]-1].append(parent_info[1])
            y_axis_list[parent_info[2]-1].append(float(line[4]))

    print("Parent time list -> len: {}; {}".format(len(x_axis_list), x_axis_list))
    print("CellID time list -> len: {}; {}".format(len(y_axis_list), y_axis_list))

    # Define a function to plot 2D histogram (irre)
    def PlotScatter(zoom=False, show=show):

        # Plot the thing:
        plt.figure()
        for gen in [1, 2, 3]:
            plt.scatter(x=x_axis_list[gen-1], y=y_axis_list[gen-1], alpha=0.7,
                        label="Generation #{}\n{} parent_IDs".format(gen, len(x_axis_list[gen-1])))
            plt.title("Scatter Plot of {} cells\n(divided by generations)".format(exp_type))
            plt.xlabel("Parent division time [hours]")
            plt.ylabel("Child division time [hours]")
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
            plt.grid(b=True, color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
            if zoom is True:
                st, en = 10, 35
                plt.plot([st, en], [st, en], color="grey", linestyle="dashed", alpha=0.5)
                plt.xlim(st, en)
                plt.xticks(list(range(st, en + 1, 2)))
                plt.ylim(st, en)
                plt.yticks(list(range(st, en + 1, 2)))
                tag = "_zoom"
            else:
                plt.legend()
                tag = ""

        # Save the figures:
        directory = "/Volumes/lowegrp/Data/Kristina/{}/".format(exp_type)
        plt.savefig(directory + "Scatter_Plot_by_Gen{}.jpeg".format(tag), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    # Define a function to plot the thing:

    def PlotHist2D(bins_st=12, bins_en=24, step=1, show=show):

        # Define number of bins:
        n_bins = list(range(bins_st * 100, bins_en * 100 + int(step * 100), int(step * 100)))
        n_bins = [item/100 for item in n_bins]

        # Plot the thing:
        plt.figure()
        plt.hist2d(x=x_axis_list, y=y_axis_list, bins=n_bins)
        plt.colorbar()
        plt.title("Joint Probability 2D Histogram\n{} on {} Cell_IDs (mixed generations)".format(exp_type, len(x_axis_list)))
        plt.xlabel("Parent division time [hours]")
        plt.ylabel("Child division time [hours]")
        # TODO: Implement the plt.plot as in 'Joint_Probab_Hist2D' script without x= and y=!
        #plt.scatter(x=n_bins, y=n_bins, color="white", s=2, alpha=0.3)
        #plt.plot(x=n_bins, y=n_bins, color="white", zorder=20)

        # Save the figures:
        directory = "/Volumes/lowegrp/Data/Kristina/{}/".format(exp_type)
        step = str(step).replace(".", "")
        plt.savefig(directory + "Hist2D_Range_{}-{}-{}.jpeg".format(bins_st, bins_en, step), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    #PlotHist2D(bins_st=10, bins_en=35, step=1.0)
    #PlotHist2D(bins_st=10, bins_en=35, step=0.2)
    #PlotHist2D(bins_st=16, bins_en=24, step=0.5)
    #PlotHist2D(bins_st=10, bins_en=35, step=2.5)

    PlotScatter(zoom=False)
    PlotScatter(zoom=True)


PlotJointProbabHistCCT(exp_type="MDCK_WT_Pure", show=True)