# TODO: Plot the histograms of individual generations of MDCK cells:

# [cell_ID (int), pos (str), date (str), cell_type (str), fate (int),
#  frm_st (int), frm_en (int), cct[min] (float), cct[hrs] (float),
#  gen (int), root (int), parent (int), child_1 (int), child_2 (int)]

import matplotlib.pyplot as plt
import numpy as np

txt_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/overall_analysis/cellIDdetails_MDCK_merged.txt"


# Plot the histogram for all cells across generations 1-5:

cct = [[] for _ in range(10)]

for line in open(txt_file, 'r'):
    line = line.rstrip().split("\t")
    #if float(line[8]) < 5.0:
    #   continue
    cct[int(line[9])].append(float(line[8]))


colors = ["dodgerblue", "orange", "forestgreen", "firebrick", "purple"]
for enum, gen in enumerate(cct[1:6]):
    a, b, c =plt.hist(x=gen, bins=40, range=(5.0, 45.0), color=colors[enum], alpha=0.5, label="Gen #{}".format(enum+1))
    plt.axvline(x=np.mean(gen), ls='dashed', color=colors[enum])
    print (a, b)


plt.legend(loc="best")
plt.show()
plt.close()

# ---------------------

# Plot the histogram for cells in generation 4 reversibly up to generation 1:

cell = []
cct = []
parent = []
root = []


for line in open(txt_file, 'r'):
    line = line.rstrip().split("\t")
    if int(line[9]) == 4:
        cell.append(int(line[0]))
        cct.append(float(line[8]))
        parent.append(int(line[11]))
        root.append([int(line[10]), line[1], line[2]])

print (cell[0])
print (cct[0])
print (parent[0])
print (root[0])
