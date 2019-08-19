# TODO: Calculate linear regression line parameters for linear bins in the Sandler-way of plotting CCT:

"""
x = [8, 9, 10]
y = [20.249543568464727, 21.877925925925926, 23.047960199004972]

result = linregress(x, y)
print (result)
"""

# ------------------------

#Plot the mean cell cycle duration as in Sandler et al., 2015 - supplementary data

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp
from scipy.stats import linregress
from itertools import chain


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


# Extract frame & CCT info from the bins where graph becomes linear (i.e. bin 700-800, 800-900 and 900-1000):
bin_mean_frame = []
bin_mean_cct_h = []
frame_list = [[] for i in range(3)]
cct_h_list = [[] for i in range(3)]
for index, bin in enumerate(hist_bins):
    if index >= 7 and index <= 9:
        print (index, len(bin), bin)
        for element in bin:
            frame_list[index-7].append(element[1])
            cct_h_list[index-7].append(element[2])
        bin_mean_frame.append([index, np.mean(frame_list[index-7]), sp.sem(frame_list[index-7])])
        bin_mean_cct_h.append([index, np.mean(cct_h_list[index-7]), sp.sem(cct_h_list[index-7])])

print (bin_mean_frame)
print (bin_mean_cct_h)
print (frame_list)
print (cct_h_list)


# Plot the thing:
color_list = ["blue", "orange", "green"]

    # Raw Data:
for index, (mini_x, mini_y) in enumerate(zip(frame_list, cct_h_list)):
    plt.scatter(x=mini_x, y=mini_y, color=color_list[index], alpha=0.3, label="Bin #{}".format(index + 7))

result_raw = linregress(x = list(chain.from_iterable(frame_list)), y=list(chain.from_iterable(cct_h_list)))
print ("Raw data result: {}".format(result_raw))
result_raw = [round(number, 3) for number in result_raw]

plt.plot([650, 1050], [result_raw[0] * 650 + result_raw[1], result_raw[0] * 1050 + result_raw[1]], color="grey",
          linestyle='dotted', linewidth=2)
          #label="Raw Regression y = {}x + {}, R^2 = {}".format(result_raw[0], result_raw[1], result_raw[2]**2)

    # Mean Data:
for index, (mini_x, mini_y) in enumerate(zip(bin_mean_frame, bin_mean_cct_h)):
    plt.scatter(x=mini_x, y=mini_y, s=200, color="dark"+color_list[index], edgecolor='silver', linewidth='3',
                label="Mean per Bin #{}".format(index + 7))
    plt.errorbar(x=mini_x, y=mini_y, color="dark"+color_list[index], ls='none', capsize=10)

result_mean = linregress(x = [bin_mean_frame[0][1], bin_mean_frame[1][1], bin_mean_frame[2][1]],
                         y = [bin_mean_cct_h[0][1], bin_mean_cct_h[1][1], bin_mean_cct_h[2][1]])
print ("Mean data result: {}".format(result_mean))
result_mean = [round(number, 3) for number in result_mean]
plt.plot([650, 1050], [result_mean[0] * 650 + result_mean[1], result_mean[0] * 1050 + result_mean[1]], color="grey",
          linestyle='dashed', linewidth=2)
          #label="Mean Regression y = {}x + {}, R^2 = {}".format(result_mean[0], result_mean[1], result_mean[2]**2)


plt.xticks(rotation=45)
plt.xlabel("T-mid [frame]")
plt.title("Mean Cell Cycle Duration - Linear Bins - 'MDCK_WT_Pure'")
plt.ylabel("Cell Cycle Duration [mean ± s.e.m.]")
plt.xlim(680, 1020)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=2)
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Mean_CCT_Sandler_Method_Linear_Regression.jpeg", bbox_inches = "tight")
plt.show()
plt.close()