#TODO: Calculate & plot the cell count per each individual frame:

# Output 2 lists:
    # cell_ID_frame_list -> [[0, 1, 2, ...], [0, 1, 2, ...], ...]
    # concat_frame_list -> [0, 1, 2, ..., 0, 1, 2, ..., ...]


# Read from GenTree_Functions-written file:

cell_ID_list = []
cell_ID_frame_list = []
for line in open("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Analysis-17_07_31-Pos8_All_Cells_ver4.txt", "r"):
    line = line.rstrip().split("\t")
    if line[0] == 'Cell_ID':
        continue
    frm_st = int(line[1])
    frm_en = int(line[2])
    cell_ID_list.append(int(line[0]))
    cell_ID_frame_list.append(list(range(frm_st, frm_en + 1)))  # includes the last frame
    if frm_st > frm_en:
        raise Exception("Warning, frameAppears ({}) > frameDisappears ({}) ! Tracking error!".format(frm_st, frm_en))
concat_frame_list = sum(cell_ID_frame_list, [])


# Plot a figure ->
# subplot 1 = scatter graph depicting the number of cells present in each frame
# subplot 2 = lined graph depicting the frames covered by the particular cell_ID


# ----- Subplot 1 axes:

x_axis_1 = list(range(1, 1200 + 1))
y_axis_1 = []

for frame in x_axis_1:
    y_axis_1.append(concat_frame_list.count(frame))

print ("Subplot 1: x-axis -> length: {}; {}".format(len(x_axis_1), x_axis_1))
print ("Subplot 1: y-axis -> length: {}; {}".format(len(y_axis_1), y_axis_1))

#TODO: Finish this!
for frame, count in reversed(zip(x_axis_1, y_axis_1)):
    print (frame, count)
    break

# ----- Subplot 2 axes:
"""
x_axis_2 = cell_ID_frame_list
y_axis_2 = []

for cell_ID, frame_list in zip(cell_ID_list, cell_ID_frame_list):
    y_axis_2.append([cell_ID] * len(frame_list))

print ("Subplot 2: x-axis -> length: {}; {}".format(len(x_axis_2), x_axis_2))
print ("Subplot 2: y-axis -> length: {}; {}".format(len(y_axis_2), y_axis_2))


#TODO: Find out how to plot 2 x-axes (frame, hours).
"""


import matplotlib.pyplot as plt
import numpy as np

# Plot 1:
plt.scatter(x_axis_1, y_axis_1)
plt.xticks(np.arange(0, 1201, step=200))
plt.xlabel('Frame number')
plt.ylabel('Cell count')
plt.title('Cell count per frame')
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Cell_Count_per_Frame_All_Cells_ver4.jpeg", bbox_inches = "tight")
plt.show()


"""
# Plot 2:
for index, (mini_list_x, mini_list_y) in enumerate(zip(x_axis_2, y_axis_2)):
    plt.plot(x_axis_2[index], y_axis_2[index])
plt.xlabel('Frame number')
plt.ylabel('Cell ID label')
plt.title('Cell ID label per frame')
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Cell_ID_Label_per_Frame_All_Cells_ver4.jpeg", bbox_inches = "tight")
plt.show()

"""