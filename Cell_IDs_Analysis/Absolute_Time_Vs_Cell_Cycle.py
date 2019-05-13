#TODO: Plot absolute time vs cell cycle duration:

x_axis = list(range(0, 4801, 400))   # time [mins]
print (x_axis)

x_axis_3 = []
y_axis_3 = []
for line in open("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Analysis-17_07_31-Pos8_All_Cells_ver4.txt", "r"):
    line = line.rstrip().split("\t")
    if line[0] == 'Cell_ID':
        continue
    cct_m = int(line[3])
    frm_0 = int(line[1]) * 4
    x_axis_3.append(frm_0)
    y_axis_3.append(cct_m)


import matplotlib.pyplot as plt
plt.scatter(x_axis_3, y_axis_3, alpha=0.3)
plt.xlim(-200, 5000)
plt.xticks(x_axis)
plt.xlabel("Absolute time [mins]")
plt.ylabel("Cell cycle time [mins]")
plt.title("Absolute time vs cell cycle duration")
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Absolute_Time_per_Cell_Cycle_Time_All_Cells_ver4.jpeg", bbox_inches = "tight")
plt.show()
