import matplotlib.pyplot as plt
import numpy as np

def PlotJointProbabHistCCT(exp_type="MDCK_WT_Pure", show=False):
    """ Joint probability histograms with plt.hist2D on 'cellIDdetails_merged.txt' file.

    Args:
        exp_type (string)   -> "MDCK_WT_Pure" by default

    Return:
        None.
        Visualises the hist2D.
    """

    # Define a function to find a parent of each cell if cell is in gen#2 or above (to get real div.time of non-root parent)
    def FindCellParent(cell_ID):
        cell_ID = cell_ID.split("-")
        date, pos, cell = cell_ID[-1], cell_ID[-2], cell_ID[-3]
        raw_file = "/Volumes/lowegrp/Data/Kristina/{}/{}/{}/analysis/cellIDdetails_filtered.txt" \
                    .format(exp_type, date, pos)

        # TODO: Remove this conditional statement after 'cellIDdetails_merged.txt' is re-done!
        if "pos11" in raw_file or "pos12" in raw_file or "pos13" in raw_file:
            print ("Warning, movie no longer included!")
            return [int(cell), "NaN"]

        finding = False       # 'finding' is a marker => from this moment, look for 0 (so it doesn't return first 0 in file)
        for line in open(raw_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or len(line) < 8:
                continue
            if int(line[0]) == int(cell):
                finding = True
                generation = int(line[5])
            if finding is True and int(line[5]) == generation - 1:
                if generation > 1:
                    return [int(line[0]), float(line[4])]
                else:
                    return [int(line[0]), "NaN"]


    # Call the function - create 2 lists:
    merged_file = "/Volumes/lowegrp/Data/Kristina/{}/cellIDdetails_merged.txt".format(exp_type)
    x_axis_list, y_axis_list = [], []

    for line in open(merged_file, 'r'):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or len(line) < 8:
            continue
        parent_info = FindCellParent(cell_ID=line[0])
        if parent_info is not None and parent_info[1] != "NaN" and isinstance(parent_info[1], float):
            x_axis_list.append(parent_info[1])
            y_axis_list.append(float(line[4]))

    print("Parent time list -> len: {}; {}".format(len(x_axis_list), x_axis_list))
    print("CellID time list -> len: {}; {}".format(len(y_axis_list), y_axis_list))


    # Do sanity check for overwriting - count the number of lines:
    counter = 0
    for line in open(merged_file, 'r'):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or len(line) < 8:
            continue
        if int(line[5]) > 1:
            print(line)
            counter += 1
    print("Counter: {}".format(counter))
    print(len(x_axis_list) == len(y_axis_list) == counter)

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


    PlotHist2D(bins_st=10, bins_en=35, step=1.0)
    PlotHist2D(bins_st=10, bins_en=35, step=0.2)
    PlotHist2D(bins_st=16, bins_en=24, step=0.5)
    PlotHist2D(bins_st=10, bins_en=35, step=2.5)


PlotJointProbabHistCCT(exp_type="MDCK_WT_Pure", show=True)