# TODO: Plot a 'stacked' barplot (for each 'cellIDdetails_sorted.txt' file):

import matplotlib.pyplot as plt
import numpy as np
import os

def VisualiseCellIDRelabelling(txt_file, show=False):
    """ Plot the barplot for each 'cellIDdetails_sorted.txt' file
        to see how many cellIDs get re-labelled at each frame.

    Args:
        txt_file (string)       -> absolute directory to 'cellIDdetails_sorted.txt' (preferrably)

    Return:
        None.
        Visualises a figure & saves it in specified directory.

    """

    directory = str(txt_file).split("/")[:-1]
    directory = "/".join(directory) + "/movie/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    movie_length = 1200         # TODO: import this information from 'summary_movies.txt' according to the movie name!
    frame_appear = []
    frame_ceased = []

    for line in open(txt_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID":
            continue
        # Aim for Root & Leaf cells only:
        if line[6] == "True" and line[7] == "True":
            frame_appear.append(int(line[1]))
            frame_ceased.append(int(line[2]))

    # Count how many times each frame is mentioned in the created lists:
    frame_list = list(range(0, movie_length, 1))
    axis_frames = [item + 1 for item in frame_list]
    axis_appear = []
    axis_ceased = []

    for frame in frame_list:
        axis_appear.append(frame_appear.count(frame))
        axis_ceased.append(frame_ceased.count(frame))

    # Modify 'axis_appear' list to shift it one item to the left relative to 'axis-cease' list:
    cells_start = axis_appear.pop(0)    # remove the starting count of cells
    axis_appear = axis_appear + [0]     # add 0 to the end to even the lengths of the axes lists

    print ("Seeded cells: cell count at the 1st frame: {}".format(cells_start))
    print ("X-Axis: len = {}\t{}".format(len(axis_frames), axis_frames))
    print ("Y-Axis Appear: len = {}\t{}".format(len(axis_appear), axis_appear))
    print ("Y-Axis Ceased: len = {}\t{}".format(len(axis_ceased), axis_ceased))

    # Create return vector to check for odd frames where a lot of re-labelling happens:
    odd_frames = []
    cut_off = 20
    for index, (i, j) in enumerate(zip(axis_appear, axis_ceased)):
        if i > cut_off or j > cut_off:
            odd_frames.append(index + 1)

    # Do these odd frames come in pairs?
    odd_pairs = 0
    current_frame = 0
    for number in odd_frames:
        if number == current_frame + 1:
            odd_pairs += 1
        current_frame = number

    percentage = round(float(odd_pairs) / (len(odd_frames) / 2) * 100, 2)
    print ("{}% of odd frames (where over {} cellIDs are re-labelled) come in pairs.".format(percentage, cut_off))


    # Plot the thing:

        # Full-sized figure:
    plt.figure(figsize=(8, 6))
    plt.bar(x=np.array(axis_frames)-0.2, height=axis_ceased, width=0.4, color="green", label="Cells ceasing at frame 'n'")
    plt.bar(x=np.array(axis_frames)+0.2, height=axis_appear, width=0.4, color="orange", label="Cells appearing at frame 'n+1'")
    plt.title("CellID 're-labelling' issue by the tracker (v0.2.9)"
              "\n{} Root & Leaf cellIDs only included; {} seeded cells at 1st frame".format(len(frame_ceased), cells_start))

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)      # bbox_to_anchor (tuple) -> (x-axis, y-axis)
    plt.ylim(-5, 205)      # TODO: Interrupt the y-axis to plot frame 1200 y-value.
    plt.ylabel("Count of cellIDs ceased/appearing")
    plt.xlabel("Frame number")
    plt.xticks(list(range(0, movie_length + 200, 200)))

        # Detailed figure:
    start, end = 0, 20
    sub_axes = plt.axes([0.17, 0.5, 0.5, 0.35])       # left, bottom, width, height
    sub_axes.bar(x=np.array(axis_frames[start:end])-0.2, height=axis_ceased[start:end], width=0.4, color="green")
    sub_axes.bar(x=np.array(axis_frames[start:end])+0.2, height=axis_appear[start:end], width=0.4, color="orange")
    sub_axes.grid(b=None, which='major', axis='y')
    sub_axes.set_xticks(np.array(range(start + 1, end + 1)))
    sub_axes.set_ylim(-0.2)

        # Save, show & close:
    plt.savefig(directory + "CellID_Relabelling.jpeg", bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()

    return odd_frames


# Call the function:
# odd_frames = VisualiseCellIDRelabelling("/Users/kristinaulicna/Documents/Rotation_2/17_07_24-pos6/cellIDdetails_sorted.txt", show=False)
# print ("Odd frames: {}".format(odd_frames))