# TODO: Plot 2 graphs:
# 1.) Hist showing the difference between child & parent doubling time (each parent twice) - figure with 2 plots
# 2.) Hist comparing the sibling division time - figure with 2 plots

import matplotlib.pyplot as plt
import sys
sys.path.append("../")

from Cell_Cycle_Duration.Find_Family_Class import FindFamily

txt_file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos6/cellIDdetails_filtered.txt"

# Get the division time of the cells:

child_list = []
parent_list = []
sibling_1_list = []
sibling_2_list = []

for line in open(txt_file, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 8:
        continue
    cell_ID = int(line[0])
    cell_cct = float(line[4])
    generation = int(line[5])
    isLeaf = line[7]
    if generation > 1:
        parent = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindParent()
        child_list.append([cell_ID, cell_cct])
        parent_list.append(parent)
    # Must filter for leaf cells later!
    sibling = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindSibling()
    sibling_1_list.append([cell_ID, cell_cct])
    sibling_2_list.append(sibling)

print (child_list)
print (parent_list)
print (sibling_1_list)
print (sibling_2_list)


# PLOT #1: Calculate differences or ratios: parent '-' or '/' child:

difference_list = []
ratio_list = []

for parent, child in zip(parent_list, child_list):
    difference_list.append(round(parent[1] - child[1], 2))
    ratio_list.append(round(parent[1] / child[1], 2))

print (difference_list)
print (ratio_list)

# Plot the thing:
plt.hist(x=difference_list)
plt.title("Difference")
plt.show()

plt.hist(x=ratio_list)
plt.title("Ratio")
plt.show()

plt.close()


# PLOT #2: Calculate differences or ratios: sibling_1 '-' or '/' sibling_2:

sibling_diff_list = []
sibling_ratio_list = []

for sibling_1, sibling_2 in zip(sibling_1_list, sibling_2_list):
    if isinstance(sibling_1[1], float) and isinstance(sibling_2[1], float):
        sibling_diff_list.append(round(sibling_1[1] - sibling_2[1], 2))
        sibling_ratio_list.append(round(sibling_1[1] / sibling_2[1], 2))

print (sibling_diff_list)
print (sibling_ratio_list)

# TODO: Find out if absolute value is a good idea to use!
sibling_diff_list = [abs(item) for item in sibling_diff_list]

# Plot the thing:
plt.hist(x=sibling_diff_list)
plt.title("Difference Siblings (abs())")
plt.show()

plt.hist(x=sibling_ratio_list)
plt.title("Ratio Siblings")
plt.show()

plt.close()