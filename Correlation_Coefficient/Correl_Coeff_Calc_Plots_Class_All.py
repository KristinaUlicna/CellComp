# TODO: Create a class which will plot several graphs & calculate correlation coefficient for 2 sets of data:

# TODO: Calculate and/or plot the following:
# - correlation coefficient
# - scatter plot (generation-dependent)
# - histogram 2D (try to normalise to a probability histogram)
# - TODO frequency histograms
# - TODO DIRECTIONAL difference
# - TODO ratio
# - TODO probability 2D hist

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("../")

from Cell_Cycle_Duration.Find_Family_Class import FindFamily


class Correlation(object):
    """ Class to calculate correlation coefficient between 2 sets of data
        (e.g. parent CCT and child CCT) and plots the following:
            - scatter plot (generation-dependent)
            - histogram 2D (try to normalise to a probability histogram)
            - TODO frequency histograms
            - TODO DIRECTIONAL difference
            - TODO ratio
            - TODO probability 2D hist

    Args:
        CAPITALISE EACH WORD!
        x_cct (string) -> who are you comparing? e.g. "Parent" or "Grandparent" or "Sibling_1"
        y_cct (string) -> to whom are you comparing? e.g. "Child" or "Grandchild" or "Sibling_2"

    Return:
        coeff (float) -> numerical value for correlation coefficient

    """

    def __init__(self, x_type, y_type):

        self.merged_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"
        self.x_type = x_type
        self.y_type = y_type
        self.coeff = 0
        self.x_data_details = []
        self.y_data_details = []
        self.x_cct = []
        self.y_cct = []


    def CalculateCorrCoeff(self):

        x_data_details = []
        y_data_details = []

        for line in open(self.merged_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] != "Cell_ID-posX-date":
                if int(line[5]) > 1:
                    y_data = [int(line[0].split("-")[0]), float(line[4]), int(line[5])]
                    y_data_details.append(y_data)
                    if self.x_type == "Parent":
                        x_data = FindFamily(cell_ID=line[0], filtered_file=self.merged_file).FindParent()
                    elif self.x_type == "Grandparent":
                        x_data = FindFamily(cell_ID=line[0], filtered_file=self.merged_file).FindGrandparent()
                    elif self.x_type == "Sibling_1":
                        x_data = FindFamily(cell_ID=line[0], filtered_file=self.merged_file).FindSibling()
                    else:
                        x_data = [None, None, None]
                    x_data_details.append(x_data)

        self.x_data_details = x_data_details
        self.y_data_details = y_data_details

        print("{} details: {}".format(self.x_type, x_data_details))
        print("{} details: {}".format(self.y_type, y_data_details))

        # Create vectors of CCT for parent (=x) and for child (=y):
        for item_1, item_2 in zip(x_data_details, y_data_details):
            if item_1[1] != "NaN" and item_2[1] != "NaN" and item_1[1] != None and item_2[1] != None:
                self.x_cct.append(item_1[1])
                self.y_cct.append(item_2[1])

        print("{} CCT: {}".format(self.x_type, self.x_cct))
        print("{} CCT: {}".format(self.y_type, self.y_cct))

        # Calculate correlation coefficient:
        coeff = np.corrcoef(x=self.x_cct, y=self.y_cct)
        self.coeff = coeff[0][1]
        print(self.coeff)

        return self.coeff


    def PlotScatter(self, show=False, min=10, max=35):
        color_list = ["dodgerblue", "orange", "green"]
        for x_point, y_point in zip(self.x_data_details, self.y_data_details):
            if x_point[1] != None and y_point[1] != None and x_point[1] != "NaN" and y_point[1] != "NaN":
                plt.scatter(x=x_point[1], y=y_point[1], c=color_list[x_point[2] - 1], alpha=0.5)
        handles_list = []
        for order, color in enumerate(color_list):
            handles_list.append(mpatches.Patch(color=color, alpha=0.5, label="Gen #{}".format(order + 1)))
        plt.plot([1, 50], [1, 50], color="grey", linestyle="dashed")

        plt.suptitle("{} vs {} - Cell Cycle Duration (generation-dependent)\nCorrelation Coefficient = {}"
                  .format(self.x_type, self.y_type, self.coeff), y=1.05)
        plt.tight_layout()
        plt.xlabel("{} CCT [hours]".format(self.x_type))
        plt.ylabel("{} CCT [hours]".format(self.y_type))
        plt.xlim(min, max)
        plt.ylim(min, max)
        plt.legend(handles=handles_list, loc='center left', bbox_to_anchor=(1, 0.5))

        # Initialise the text:
        if self.y_type == "Sibling_2":
            plt.text(30, 12.5, 'Green Cell ID Pair #4682 & #4683\n(Tree Root ID= #595)',
                     bbox=dict(facecolor='green', alpha=0.5), horizontalalignment='center', verticalalignment='center')
        else:
            plt.text(30, 12.5, '{} CCT >>> {} CCT\n(expected due to higher cell density)'.format(self.y_type, self.x_type),
                     bbox=dict(facecolor='silver', alpha=0.5), horizontalalignment='center', verticalalignment='center')

        plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/{}_{}_Scatter.jpeg"
                     .format(self.x_type, self.y_type), bbox_inches="tight")
        if show is True:
            plt.show()
            plt.close()


    def PlotHistogram2D(self, show=False, min=10, max=35):

        bin_no = (max - min) / 2.5
        plt.hist2d(x=self.x_cct, y=self.y_cct, bins=(bin_no, bin_no), range=[[min, max], [min, max]])
        plt.title("{} vs {} - Cell Cycle Duration (generation-independent)\nCorrelation Coefficient = {}"
                  .format(self.x_type, self.y_type, self.coeff))
        plt.xlabel("{} CCT [hours]".format(self.x_type))
        plt.ylabel("{} CCT [hours]".format(self.y_type))
        plt.colorbar()

        plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/{}_{}_Hist2D.jpeg"
                    .format(self.x_type, self.y_type), bbox_inches="tight")

        if show is True:
            plt.show()
            plt.close()
