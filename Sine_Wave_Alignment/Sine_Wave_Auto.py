import matplotlib.pyplot as plt
import numpy as np
import itertools
import sys
sys.path.append("../")

from Cell_Cycle_Duration.Find_Family_Class import FindFamily

def AlignToSinusoid(generations=3, show=True):
    """ Function to align the cell cycle durations onto a sinusoid (=sine wave)
        and visualise the relationships of multiple generations as periodical.

    Args:
        generations (int) -> number of generations you want to visualise.
        show (boolean) -> show or hide the final plot.

    Return:
        gen_1_list, gen_2_list, gen_3_list
            -> lists of lists [[cell_ID, CCT-hours, generation], [..., ..., ...], ...]
    """

    if generations != 2 and generations != 3:
        raise Exception("Warning, the function is only optimised for 2- or 3-generational relationships")

    # ---------- Generate vectors to start with:

    merged_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"

    gen_3_list = []
    gen_2_list = []
    gen_1_list = []

    counter = 0
    for line in open(merged_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Cell_ID-posX-date":
            if generations == 3:
                if int(line[5]) == 3:
                    counter += 1
                    call = FindFamily(cell_ID=line[0], filtered_file=merged_file)
                    gen_3_list.append(call.FindItself())
                    gen_2_list.append(call.FindParent())
                    gen_1_list.append(call.FindGrandparent())
            if generations == 2:
                if int(line[5]) == 2 or int(line[5]) == 3:
                    counter += 1
                    call = FindFamily(cell_ID=line[0], filtered_file=merged_file)
                    gen_2_list.append(call.FindItself())
                    gen_1_list.append(call.FindParent())

    print ("Counter: {}".format(counter))
    print ("Gen_1_list: len = {}; {}".format(len(gen_1_list), gen_1_list))
    print ("Gen_2_list: len = {}; {}".format(len(gen_2_list), gen_2_list))
    print ("Gen_3_list: len = {}; {}".format(len(gen_3_list), gen_3_list))


    # ---------- Sine wave definition:

    fs = 80                             # sample rate
    f = 2                               # the frequency of the signal

    x = np.arange(0, fs+1, 1)           # the points on the x axis for plotting
    y = np.sin(2*np.pi*f * (x/fs))      # compute the value (amplitude) of the sin wave at the for each sample

    plt.plot(x, y, "r-")


    # ---------- Plot the generational CCTs on top of the sine wave:

    counter = 0
    for l1, l2, l3 in list(itertools.zip_longest(gen_1_list, gen_2_list, gen_3_list)):
        counter += 1

        # Gen#1:
        l1_x1 = 10 - (l1[1] / 2)
        l1_x2 = 10 + (l1[1] / 2)
        y = np.sin(2 * np.pi * f * (l1_x1 / fs))
        plt.plot([l1_x1, l1_x2], [y, y], marker="o", color="blue", alpha=0.3)

            # Gen#2:
        l2_x1 = l1_x2
        l2_x2 = l1_x2 + l2[1]
        plt.plot([l2_x1, l2_x2], [y, y], marker="o", color="orange", alpha=0.3)

        if generations == 3:
                # Gen#3:
            l3_x1 = l2_x2
            l3_x2 = l2_x2 + l3[1]
            plt.plot([l3_x1, l3_x2], [y, y], marker="o", color="green", alpha=0.3)

    # Decorate the graph:
    plt.grid(axis="both")
    plt.title("Fitting Generational CCT ({} cell_IDs) on Sine Wave".format(counter))
    plt.xlabel("Time [hours]")
    plt.ylabel("Amplitude")

    # Save, visualise & close:
    plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave_Fitting_{}cells.jpeg".format(counter), bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()

    return gen_1_list, gen_2_list, gen_3_list


AlignToSinusoid(generations=2)
AlignToSinusoid(generations=3)