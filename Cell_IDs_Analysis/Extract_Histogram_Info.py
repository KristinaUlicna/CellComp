# TODO: Extract cells which have certain cell_cycle_durations:
# TODO: Remove hardcoding!!! Number of generations does not necessarily need to be 5!

from Analysis_And_Plotting_Class import *
import matplotlib.pyplot as plt
import numpy as np


def PlotCCTvsGenDependence(txt_file):
    # Explore the file: only use those lines that give you an actual
    # file = "/Users/kristinaulicna/Documents/Rotation_2/cellIDinfo_vertest.txt"
    cell_cycle_duration = [[] for i in range(5)]

    for line in open(file, 'r'):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID":
            #print (line)
            continue
        #if line[6] == "False" and line[7] == "False" and float(line[4]) <= 4:
        if line[6] == "False" and line[7] == "False":
            print (line)
            cell_cycle_duration[int(line[5])-1].append(float(line[3]))
    print ("Cell_cycle_duration:\t{}".format(cell_cycle_duration))

    # Figure out the means & stdev of the values for each generation:
    means = [round(np.mean(mini_list), 2) for mini_list in cell_cycle_duration]
    #print (means)
    stdev = [round(np.std(mini_list), 2) for mini_list in cell_cycle_duration]
    #print (stdev)
    n_num = ["n={}".format(len(mini_list)) for mini_list in cell_cycle_duration]

    # Plot the thing:
    plt.bar(x=list(range(1, 6)), height=means, yerr=stdev, color="olive", ecolor="y")
    plt.xlabel("Generation i.e number of mitoses underwent")
    plt.ylabel("Cell Cycle Duration [mins]")
    plt.title("Is there a dependence of the cell cycle duration on the generation?")
    plt.text(x=list(range(1, 6)), y=means, s=n_num)
    plt.show()


# TODO: What are these graphs showing you?
# Iterate through verX files:
file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracker_Updates_XML_Files/ver4/cellIDinfo_ver4.txt"
PlotCCTvsGenDependence(txt_file=file)