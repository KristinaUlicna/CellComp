#TODO: Calculate & plot the cell count per each individual frame:

from GenTree_Functions import *

cell_ID_frame_list = []
for i in list(range(0, 10)):
    cell_ID, _, _, _, _, frameAppears, frameDisappears, _, _, _, _, _, _ = GetCellDetails(cell_ID=i, pos=8)
    if frameAppears is not None and frameDisappears is not None:
        cell_ID_frame_list.append(list(range(frameAppears, frameDisappears + 1)))   # includes the last frame
        if frameAppears > frameDisappears:
            raise Exception("Warning, frameAppears > frameDisappears! Tracking error!")
concat_frame_list = sum(cell_ID_frame_list, [])


#Plot:

import matplotlib.pyplot as plt
x_axis = list(range(1, 1200 + 1))
y_axis = []

for frame in range(1, 1200 + 1):
    y_axis.append(concat_frame_list.count(frame))

print (len(x_axis), x_axis)
print (len(y_axis), y_axis)

#TODO: Label the graph nicely. Create a figure rather than a plot.
plt.scatter(x_axis, y_axis)
plt.show()
plt.close()

#TODO: Create a graph with horizontal lines, depicting each cell_ID's life.
#TODO: Create a file with all of the cells detailed (call your function for range(0, 13000)
#TODO: Create the plot by reading the file instead of calling the function in this script: should take shorter time.