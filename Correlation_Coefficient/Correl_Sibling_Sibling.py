# SIBLING vs SIBLING correlation:

# TODO: Calculate and/or plot the following:
# - correlation coefficient
# - scatter plot (generation-dependent)
# - histogram 2D (try to normalise to a probability histogram)
# - frequency histograms
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


# Loop through the file to find all sibling pairs:
file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"
sibling_1_details = []
sibling_2_details = []

for line in open(file, "r"):
    line = line.rstrip().split("\t")
    if line[0] != "Cell_ID-posX-date":
        if int(line[5]) > 1:
            sibling_ID = line[0].split("-")[0]
            sibling_1 = [int(sibling_ID), float(line[4]), int(line[5])]
            sibling_1_details.append(sibling_1)
            sibling_2 = FindFamily(cell_ID=line[0], filtered_file=file).FindSibling()
            sibling_2_details.append(sibling_2)

print ("Sibling_1_details: {}".format(sibling_1_details))
print ("Sibling_2_details: {}".format(sibling_2_details))


# ---------- A L L  D A T A  (with duplicates) ----------

# Create vectors of CCT for parent (=x) and for child (=y):
sibling_1_cct = []
sibling_2_cct = []
for item_1, item_2 in zip(sibling_1_details, sibling_2_details):
    if item_1[1] != "NaN" and item_2[1] != "NaN":
        sibling_1_cct.append(item_1[1])
        sibling_2_cct.append(item_2[1])

print ("Sibling_1_cct: {}".format(sibling_1_cct))
print ("Sibling_2_cct: {}".format(sibling_2_cct))


# Calculate correlation coefficient:
coeff = np.corrcoef(x=sibling_1_cct, y=sibling_2_cct)
coeff = coeff[0][1]
print ("Correlation Coefficient of all data: {}".format(coeff))


# Plot scatter plot dependent on generation - MIRROR IMAGE:
color_list = ["dodgerblue", "orange", "green"]
for sbl_1, sbl_2 in zip(sibling_1_details, sibling_2_details):
    if sbl_1[1] != "NaN" and sbl_2[1] != "NaN":
        plt.scatter(x=sbl_1[1], y=sbl_2[1], c=color_list[sbl_1[2]-1], alpha=0.5)
handles_list = []
for order, color in enumerate(color_list):
    handles_list.append(mpatches.Patch(color=color, alpha=0.5,
                 label="Sibling Gen#{}".format(order+1)))
plt.plot([10, 40], [10, 40], color="grey", linestyle="dashed")
plt.text(32, 15, 'Green Cell ID Pair #4682 & #4683\n(Tree Root ID= #595)', bbox=dict(facecolor='green', alpha=0.5),
         horizontalalignment='center', verticalalignment='center')

plt.title("Sibling 1 vs Sibling 2 - Cell Cycle Duration\n(generation-dependent; mirror image)\nCorrelation Coefficient = {}".format(coeff))
plt.xlabel("Sibling 1 CCT [hours]")
plt.ylabel("Sibling 2 CCT [hours]")
plt.xlim(12, 33)
plt.ylim(12, 33)
plt.legend(handles=handles_list, loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/Sibling_Sibling_Duplicates_Scatter.jpeg", bbox_inches="tight")
plt.show()
plt.close()


# Plot Histogram 2D:
plt.hist2d(x=sibling_1_cct, y=sibling_2_cct, bins=(12, 12), range=[[14, 26], [14, 26]])
plt.title("Sibling 1 vs Sibling 2 - Cell Cycle Duration\n(generation-independent; mirror image)\nCorrelation Coefficient = {}".format(coeff))
plt.xlabel("Sibling 1 CCT [hours]")
plt.ylabel("Sibling 2 CCT [hours]")
plt.colorbar()
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/Sibling_Sibling_Duplicates_Hist.jpeg", bbox_inches="tight")
plt.show()
plt.close()



# ---------- R E M O V E  D U P L I C A T E S ----------

# Filter created vectors for duplicates (each sibling pair only mentioned once):
sibling_1_cct = [item for item in sibling_1_cct if sibling_1_cct.index(item) % 2 == 0]
sibling_2_cct = [item for item in sibling_2_cct if sibling_2_cct.index(item) % 2 == 0]

print ("Sibling_1_cct: {}".format(sibling_1_cct))
print ("Sibling_2_cct: {}".format(sibling_2_cct))


# Calculate correlation coefficient:
coeff = np.corrcoef(x=sibling_1_cct, y=sibling_2_cct)
coeff = coeff[0][1]
print ("Correlation Coefficient of all data: {}".format(coeff))


# Plot scatter plot dependent on generation - No DUPLICATES:
plt.scatter(x=sibling_1_cct, y=sibling_2_cct, alpha=0.5, color="firebrick")
plt.plot([10, 40], [10, 40], color="grey", linestyle="dashed")
plt.text(33.5, 14, '"Each Sibling Pair\nappearing only once"', bbox=dict(facecolor='silver', alpha=0.5),
         horizontalalignment='center', verticalalignment='center')

plt.title("Sibling 1 vs Sibling 2 - Cell Cycle Duration\n(generation-dependent; no duplicates)\nCorrelation Coefficient = {}".format(coeff))
plt.xlabel("Sibling 1 CCT [hours]")
plt.ylabel("Sibling 2 CCT [hours]")
plt.xlim(11, 30)
plt.ylim(12.5, 33)
plt.legend(handles=[mpatches.Patch(color="firebrick", alpha=0.5, label="Sibling Pair\nGen #2")], loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/Sibling_Sibling_RemovedDupl_Scatter.jpeg", bbox_inches="tight")
plt.show()
plt.close()


# Plot Histogram 2D:
plt.hist2d(x=sibling_1_cct, y=sibling_2_cct, bins=(12, 12), range=[[14, 26], [14, 26]])
plt.title("Sibling 1 vs Sibling 2 - Cell Cycle Duration\n(generation-independent; no duplicates)\nCorrelation Coefficient = {}".format(coeff))
plt.xlabel("Sibling 1 CCT [hours]")
plt.ylabel("Sibling 2 CCT [hours]")
plt.colorbar()
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/Sibling_Sibling_RemovedDupl_Hist.jpeg", bbox_inches="tight")
plt.show()
plt.close()



