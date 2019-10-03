#Plot the mean cell cycle duration as in Sandler et al., 2015 - supplementary data

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp

file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"

t_mid_list = []
for line in open(file, "r"):
    line = line.rstrip().split("\t")
    if line[0] != "Cell_ID-posX-date":
        t_mid = int((int(line[2]) - int(line[1])) / 2) + int(line[1])
        t_mid_list.append([line[0], t_mid, float(line[4])])

print ("T_mid values: {}".format(t_mid_list))


# A 'while' loop to divide into 12 T-mid categories:

min_val = 0
max_val = 100
counter = 0
hist_bins = [[] for i in range(12)]

while min_val < 1200 and max_val < 1200:
    for t_mid in t_mid_list:
        if t_mid[1] > min_val and t_mid[1] <= max_val:
            hist_bins[counter].append(t_mid)
    counter += 1
    min_val += 100
    max_val += 100


# Merge bin CCTs together:
value_list = [[] for i in range(12)]
length_list = []
for index, bin in enumerate(hist_bins):
    print(len(bin), bin)
    length_list.append(len(bin))
    for value in bin:
        value_list[index].append(value[2])
print ("HERE!:", value_list)


# Calculate the means & std for each category:
for index, mini_list in enumerate(value_list):
    if len(mini_list) < 3:
        value_list[index] = [0.0, 0.0, 0.0]
    else:
        value_list[index] = [np.mean(mini_list), np.std(mini_list), sp.sem(mini_list)]
print (value_list)


# Plot the thing:
labels = ["0-100", "100-200", "200-300", "300-400", "400-500", "500-600", "600-700", "700-800", "800-900", "900-1000", "1000-1100", "1100-1200"]
mean_list = []
std_list = []
sem_list = []

for lst in value_list:
    mean_list.append(lst[0])
    std_list.append(lst[1])
    sem_list.append(lst[2])

plt.plot(labels, mean_list, "ro", label="n = {}".format(length_list))
#plt.errorbar(labels, mean_list, yerr=std_list, color="dodgerblue", ls='none', capsize=10)
plt.errorbar(labels, mean_list, yerr=sem_list, color="forestgreen", ls='none', capsize=10)
#plt.annotate(length_list)
plt.xticks(rotation=45)
plt.xlabel("T-mid [frame]")
plt.title("Mean Cell Cycle Duration - 'MDCK_WT_Pure'")
plt.ylabel("Cell Cycle Duration [mean ± s.e.m.]")
plt.ylim(17, 25)
plt.legend(loc='upper left', fontsize='large')
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Mean_CCT_Sandler_Method.jpeg", bbox_inches = "tight")
plt.show()
plt.close()