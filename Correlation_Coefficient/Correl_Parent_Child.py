# PARENT vs CHILD correlation:

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

file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"


child_details = []
parent_details = []

for line in open(file, "r"):
    line = line.rstrip().split("\t")
    if line[0] != "Cell_ID-posX-date":
        if int(line[5]) > 1:
            child_ID = line[0].split("-")[0]
            child = [int(child_ID), float(line[4]), int(line[5])]
            child_details.append(child)
            parent = FindFamily(cell_ID=line[0], filtered_file=file).FindParent()
            parent_details.append(parent)

print ("Parent_details: {}".format(parent_details))
print ("Child_details: {}".format(child_details))


# Create vectors of CCT for parent (=x) and for child (=y):
parent_cct = [item[1] for item in parent_details]
child_cct = [item[1] for item in child_details]

print ("Parent_cct: {}".format(parent_cct))
print ("Child_cct: {}".format(child_cct))


# Calculate correlation coefficient:
coeff = np.corrcoef(x=parent_cct, y=child_cct)
coeff = coeff[0][1]
print (coeff)


# Plot scatter plot dependent on generation:
color_list = ["dodgerblue", "orange", "green"]
for par, chld in zip(parent_details, child_details):
    plt.scatter(x=par[1], y=chld[1], c=color_list[par[2]-1], alpha=0.5)
handles_list = []
for order, color in enumerate(color_list):
    handles_list.append(mpatches.Patch(color=color, alpha=0.5,
                 label="Parent Gen#{}\nChild Gen#{}".format(order+1, order+2)))
plt.plot([12, 30], [12, 30], color="grey", linestyle="dashed")
plt.text(27, 14, 'Children CCT >>> Parent CCT\n(expected due to cell density)', bbox=dict(facecolor='silver', alpha=0.5),
         horizontalalignment='center', verticalalignment='center')

plt.title("Parent vs Child - Cell Cycle Duration\n(generation-dependent)\nCorrelation Coefficient = {}".format(coeff))
plt.xlabel("Parent CCT [hours]")
plt.ylabel("Child CCT [hours]")
plt.xlim(12, 26)
plt.ylim(12, 32)
plt.legend(handles=handles_list, loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/Parent_Child_Scatter.jpeg", bbox_inches="tight")
plt.show()
plt.close()


# Plot Histogram 2D:
plt.hist2d(x=parent_cct, y=child_cct, bins=(6, 8), range=[[12, 24], [12, 28]])
plt.title("Parent vs Child - Cell Cycle Duration\n(generation-independent)\nCorrelation Coefficient = {}".format(coeff))
plt.xlabel("Parent CCT [hours]")
plt.ylabel("Child CCT [hours]")
plt.colorbar()
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/Parent_Child_Hist2D.jpeg", bbox_inches="tight")
plt.show()
plt.close()