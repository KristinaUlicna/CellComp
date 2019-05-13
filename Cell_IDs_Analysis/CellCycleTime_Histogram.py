#TODO: Plot a histogram of cell cycle times:

cct_hrs = []
cct_hrs_less10 = []
cct_hrs_less2 = []
for line in open("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Analysis-17_07_31-Pos8_All_Cells_ver4.txt", "r"):
    line = line.rstrip().split("\t")
    if line[0] == 'Cell_ID':
        continue
    cct = float(line[4])
    cct_hrs.append(cct)
    if cct <= 10.0:
        cct_hrs_less10.append(cct)
    if cct <= 2.0:
        cct_hrs_less2.append(cct)


import matplotlib.pyplot as plt

plt.hist(cct_hrs)
plt.ylim(-100)
plt.title("Cell Cycle Time [hours] of ALL Cell_IDs")
plt.xlabel("Cell Cycle Time [hours]")
plt.ylabel("Cell ID count")
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Cell_Cycle_Time_Hist_All_cells_alltimes_ver4.jpeg", bbox_inches = "tight")
plt.show()
plt.close()

plt.hist(cct_hrs_less10)
plt.ylim(-100)
plt.title("Cell Cycle Time [hours] of ALL Cell_IDs")
plt.xlabel("Cell Cycle Time [hours]")
plt.ylabel("Cell ID count")
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Cell_Cycle_Time_Hist_All_cells_lessthan10_ver4.jpeg", bbox_inches = "tight")
plt.show()
plt.close()

cct_hrs_less2 = [float(item) * 60 for item in cct_hrs_less2]
xticks = list(range(0, 120+1, 4))
plt.hist(cct_hrs_less2, bins=30)
plt.xticks(xticks, rotation=45)
plt.xlim(-5, 125)
plt.ylim(-100, 2500)
plt.title("Cell Cycle Time [mins] of ALL Cell_IDs")
plt.xlabel("Cell Cycle Time [mins]")
plt.ylabel("Cell ID count")
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Cell_Cycle_Time_Hist_All_cells_lessthan2_ver4.jpeg", bbox_inches = "tight")
plt.show()
plt.close()

#TODO: Exclude root cells and leaf cells from the histogram.
