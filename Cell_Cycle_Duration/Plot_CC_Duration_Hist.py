# TODO: Plot multiple histograms per generation into one figure. Use 'cellIDdetails_filtered.txt' as input file.

import matplotlib.pyplot as plt
import numpy as np
import math


def PlotHistGenerationCCT(txt_file, show=False):
    """ Plot multiple histograms per generation into one figure.
        Use 'cellIDdetails_filtered.txt' as input file.

    Args:
        txt_file (string)                   ->    absolute directory to 'cellIDdetails_filtered.txt'
        show (boolean, False by default)    ->    plt.show() or not...

    Return:
        None.
        Save figure in desired directory.
        Visualise histogram in SciView.
    """

    # Categorize CCT according to the generations:
    generation_list = [[]]
    for line in open(txt_file, 'r'):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID":
            continue
        gen = int(line[5])
        cct = float(line[4])               # cell cycle duration in hours
        if gen > len(generation_list):     # append by as many empty lists as are missing!
            generation_list.append(([] * (gen - len(generation_list))))
        generation_list[gen-1].append(cct)

    # Print summary:
    gen_list = []
    for gen in generation_list:
        gen_list.append(len(gen))
    print ("Generations total = {}; Length of sub-lists = {}; Whole gen list = {}".format(len(generation_list), gen_list, generation_list))

    # Some vectors for plotting:
    bins = int(math.ceil(max(sum(generation_list, [])) / 5.0)) * 5
    bin_edges = list(range(0, bins + 1, 1))

    # Plot the 'stacked' histogram:
    for number, gen in enumerate(generation_list):
        a, b, c = plt.hist(gen, bins=bin_edges, edgecolor='black', linewidth=1.0, alpha=0.5, label='Generation {}'.format(number + 1))
        #print ("Gen:", number + 1, a)
        #print ("Gen:", number + 1, b)
        #print ("Gen:", number + 1, c)
    plt.legend()                # change location to "loc='upper left'" if necessary
    plt.title("Generational Cell Cycle Duration (data filtered for roots & leaves)")

    plt.xlim()
    plt.xticks(bin_edges)
    plt.xlabel("Cell Cycle Duration [hours]")
    plt.ylim(-1)                # TODO: Set 10% ± max_y!
    plt.ylabel("Cell ID count")

    # Save, show & close:
    plt.savefig(txt_file.replace('cellIDdetails_sorted.txt', 'Hist_Generational_CCT.jpeg'), bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()

# TODO: Define bins edges in 'Tracking_Plots_Class.py'
# TODO: Merge data? Download a few from TeamViewer.
# TODO: Learn how to do a t-test!