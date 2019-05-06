#TODO: Calculate & plot the cell count per each individual frame:

# Output 2 lists:
    # cell_ID_frame_list -> [[0, 1, 2, ...], [0, 1, 2, ...], ...]
    # concat_frame_list -> [0, 1, 2, ..., 0, 1, 2, ..., ...]


# OPTION 1: Using GenTree_Functions directly:
"""
from GenTree_Functions import *
cell_ID_list = []
cell_ID_frame_list = []
for i in list(range(0, 10)):
    cell_ID, _, _, _, _, frameAppears, frameDisappears, _, _, _, _, _, _ = GetCellDetails(cell_ID=i, pos=8)
    if frameAppears is not None and frameDisappears is not None:
        cell_ID_list.append(int(cell_ID))
        cell_ID_frame_list.append(list(range(frameAppears, frameDisappears + 1)))   # includes the last frame
        if frameAppears > frameDisappears:
            raise Exception("Warning, frameAppears ({}) > frameDisappears ({}) ! Tracking error!".format(frameAppears, frameDisappears))
concat_frame_list = sum(cell_ID_frame_list, [])
"""

# OPTION 2: From GenTree_Functions-written file:

cell_ID_list = []
cell_ID_frame_list = []
for line in open("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Analysis-17_07_31-Pos8Node_8_Tree.txt", "r"):
    line = line.rstrip().split("\t")
    if line[0] == 'Cell_ID':
        continue
    if len(line) < 13:
        break
    frameAppears = int(line[5])
    frameDisappears = int(line[6])
    cell_ID_list.append(int(line[0]))
    cell_ID_frame_list.append(list(range(frameAppears, frameDisappears + 1)))  # includes the last frame
    if frameAppears > frameDisappears:
        raise Exception("Warning, frameAppears ({}) > frameDisappears ({}) ! Tracking error!".format(frameAppears, frameDisappears))
concat_frame_list = sum(cell_ID_frame_list, [])


# Plot a figure ->
# subplot 1 = scatter graph depicting the number of cells present in each frame
# subplot 2 = lined graph depicting the frames covered by the particular cell_ID


# ----- Subplot 1 axes:

x_axis_1 = list(range(1, 1200 + 1))
y_axis_1 = []

for frame in range(1, 1200 + 1):
    y_axis_1.append(concat_frame_list.count(frame))

print ("Subplot 1: x-axis -> length: {}; {}".format(len(x_axis_1), x_axis_1))
print ("Subplot 1: y-axis -> length: {}; {}".format(len(y_axis_1), y_axis_1))


# ----- Subplot 2 axes:

x_axis_2 = cell_ID_frame_list
y_axis_2 = []

for cell_ID, frame_list in zip(cell_ID_list, cell_ID_frame_list):
    y_axis_2.append([cell_ID] * len(frame_list))

print ("Subplot 2: x-axis -> length: {}; {}".format(len(x_axis_2), x_axis_2))
print ("Subplot 2: y-axis -> length: {}; {}".format(len(y_axis_2), y_axis_2))


#TODO: Find out how to plot 2 x-axes (frame, hours).

import matplotlib.pyplot as plt
import numpy as np

f, (ax1, ax2) = plt.subplots(1, 2, sharex = True)
f.suptitle('Visualisation of cell count per each movie frame')

# Subplot 1:
ax1.scatter(x_axis_1, y_axis_1)
ax1.set_xticks(np.arange(0, 1201, step=300))
ax1.set_xlabel('Frame number')
ax1.set_ylabel('Cell ID count')
ax1.set_title('Cell count per frame')

# Subplot 2:
for index, (mini_list_x, mini_list_y) in enumerate(zip(x_axis_2, y_axis_2)):
    ax2.plot(x_axis_2[index], y_axis_2[index])
ax2.set_xlabel('Frame number')
ax2.set_ylabel('Cell ID label')
ax2.set_title('Cell ID label per frame')

# Save & show the figure
plt.tight_layout()
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Cell_Count_per_Frame_Node8Cells.jpeg", bbox_inches = "tight")
plt.show()
plt.close()
