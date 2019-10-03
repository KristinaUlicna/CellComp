# TODO: Plot 2 graphs:
# 1.) Hist showing the difference between child & parent doubling time (each parent twice) - figure with 2 plots
# 2.) Hist comparing the sibling division time - figure with 2 plots

import matplotlib.pyplot as plt
import time
import os
import sys
sys.path.append("../")

from Cell_Cycle_Duration.Find_Family_Class import FindFamily
start_time = time.process_time()


def PlotParentChildCCTDiff(txt_file, show=False, print_stats=False):
    """ Plot the difference between the division time of parent - child.
        Plot the ratio --- || --- .
        Plot the difference between the siblings. Possibly absolute value?
        Plot the ratio --- || --- .

    Args:
        txt_file (string)  ->  filtered or merged file, merged preferably.
    """

    directory = txt_file.split("/")[:-1]
    directory = "/".join(directory) + "/bulk_analysis/merged_data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the division time of the cells:

    child_list = []
    parent_list = []
    sibling_list = []

    for line in open(txt_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date" or len(line) < 8:
            continue
        # FindItself()
        cell_ID = line[0]
        child_info = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindItself()
        child_list.append(child_info)
        # FindParent()
        parent_info = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindParent()
        parent_list.append(parent_info)
        # FindSibling()
        sibling_info = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindSibling()
        sibling_list.append(sibling_info)

    if print_stats is True:
        print ("\nChild (cell_ID): len = {}\t-> {}".format(len(child_list), child_list))
        print ("Parent list: len = {}\t-> {}".format(len(parent_list), parent_list))
        print ("Sibling list: len = {}\t-> {}".format(len(sibling_list), sibling_list))


    # Calculate differences & ratios: parent '-' or '/' child:

    difference_list = []
    ratio_list = []

    for parent, child in zip(parent_list, child_list):
        if parent[1] != "NaN" and child[1] != "NaN":    # non-root parent, non-leaf child...
            if parent[1] >= 5.0 and child[1] >= 5.0:    # both cells are not artefacts (divide in longer than 5.0 hours)
                if parent[2] == child[2] - 1:           # parent is exactly one generation older than child
                    difference_list.append(round(parent[1] - child[1], 2))
                    ratio_list.append(round(parent[1] / child[1], 2))
                    if abs(parent[1] - child[1]) > 10:
                        print (parent, child)

    counter_over_0 = 0
    for item in difference_list:
        if item >= 0:
            counter_over_0 += 1
    percent_total = round(counter_over_0 * 100 / len(difference_list), 2)

    if print_stats is True:
        print ("\nParent - Child (diff): len = {}; percentage = {}%\t-> {}"
               .format(len(difference_list), len(difference_list)*100/len(child_list), difference_list))
        print ("Parent / Child (ratio): len = {}; percentage = {}%\t-> {}"
               .format(len(ratio_list), len(ratio_list)*100/len(child_list), ratio_list))


    # Calculate differences & ratios: sibling_1 '-' or '/' sibling_2:

    sibling_diff_list = []
    sibling_ratio_list = []

    for child, sibling in zip(child_list, sibling_list):
        if sibling[1] != "NaN" and child[1] != "NaN":    # both cells are non-leaves
            if sibling[1] >= 5.0 and child[1] >= 5.0:    # both cells are not artefacts (divide in longer than 5.0 hours)
                if sibling[2] == child[2]:               # both cells are in the same generation
                    sibling_diff_list.append(round(child[1] - sibling[1], 2))
                    sibling_ratio_list.append(round(child[1] / sibling[1], 2))
                    if abs(child[1] - sibling[1]) > 10:
                        print (child, sibling)

    if print_stats is True:
        print ("\nSibling_1 - Sibling_2 (diff): len = {}; percentage = {}%\t-> {}"
               .format(len(sibling_diff_list), len(sibling_diff_list)*100/len(child_list), sibling_diff_list))
        print ("Sibling_1 / Sibling_2 (ratio): len = {}; percentage = {}%\t-> {}"
               .format(len(sibling_ratio_list), len(sibling_ratio_list)*100/len(child_list), sibling_ratio_list))


    # Plot the thing (all 4 on 1 figure):
    """
    fig = plt.figure()
    colors = ['dodgerblue', 'orange', 'forestgreen', 'firebrick']
    datasets = [difference_list, ratio_list, sibling_diff_list, sibling_ratio_list]

    for order, (color, data) in enumerate(zip(colors, datasets)):
        plt.subplot(2, 2, order+1)
        a, b, c = plt.hist(x=data, bins=10, color=color, edgecolor=color, linewidth=1.0, alpha=0.5)
        print (a)
        print (b)
        print (c)
        plt.title("Difference or Ratio ({} cell pairs)".format(len(data)))
        plt.xlim(-10, 10)
        plt.xlabel("Difference [hrs]")
        plt.ylim(-10)
        plt.ylabel("Cell_ID Pairs [#]")
    """

    # ---------- Plot one thing at a time:

    # Plot Difference PARENT - CHILD:
    limit = 24
    bins = list(range(-limit, limit + 1, 1))
    plt.hist(x=difference_list, bins=bins, color='dodgerblue', edgecolor='dodgerblue', linewidth=1.0, alpha=0.5)
    plt.axvline(x=0, color='grey', linestyle='dashed', linewidth=1.5)
    plt.text(-15, 50, 'Child > Parent\nEXPECTED due to\n>>> confluency', fontsize=10,
             horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='purple', alpha=0.5))
    plt.text(15, 50, 'Child < Parent\n! NON-EXPECTED !\n{} cell_IDs; {}%'.format(counter_over_0, percent_total),
             fontsize=10, horizontalalignment='center', verticalalignment='center',
             bbox=dict(facecolor='salmon', alpha=0.5))
    plt.title("Difference PARENT - CHILD\n({} cell pairs)".format(len(difference_list)))
    plt.xlim(-limit - 1, limit + 1)
    plt.xlabel("Difference [hrs]")
    plt.ylim(-5)
    plt.ylabel("Cell_ID Pairs [#]")

    # Save, show & close:
    plt.savefig(directory + "Hist_Parent_vs_Child_Diff_All.jpeg", bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()


    # Plot Ratio PARENT - CHILD:
    limit = 3
    bins = list(range(0, limit + 1, 1))
    bins = bins[-1] * 10
    plt.hist(x=ratio_list, bins=bins, color='sandybrown', edgecolor='sandybrown', linewidth=1.0, alpha=0.5)
    plt.axvline(x=1, color='grey', linestyle='dashed', linewidth=1.5)
    plt.title("Ratio PARENT - CHILD\n({} cell pairs)".format(len(ratio_list)))
    plt.xlim(0, limit)
    plt.xlabel("Ratio")
    plt.ylim(-5)
    plt.ylabel("Cell_ID Pairs [#]")

    # Save, show & close:
    plt.savefig(directory + "Hist_Parent_vs_Child_Ratio_All.jpeg", bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()


    # Plot Difference SIBLING 1 - SIBLING 2 (abs()):
    limit = 15
    bins = list(range(0, limit + 1, 1))
    siblings = [abs(item) for item in sibling_diff_list]
    plt.hist(x=siblings, bins=bins, color='firebrick', edgecolor='firebrick', linewidth=1.0, alpha=0.7)

    plt.title("Difference SIBLING 1 - SIBLING 2 (absolute value)\n({} cell pairs - included twice)".format(int(len(siblings) / 2)))
    plt.xlim(-1, limit + 1)
    plt.xlabel("Difference [hrs]")
    plt.ylim(-10)
    plt.ylabel("Cell_ID Pairs [#]")

    # Save, show & close:
    plt.savefig(directory + "Hist_Sibling1_vs_Sibling2_Diff_All.jpeg", bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()


    # Plot Ratio SIBLING 1 - SIBLING 2: TODO = inverse?
    limit = 3
    bins = list(range(0, limit + 1, 1))
    bins = bins[-1] * 10
    plt.hist(x=sibling_ratio_list, bins=bins, color='forestgreen', edgecolor='forestgreen', linewidth=1.0, alpha=0.5)
    plt.axvline(x=1, color='grey', linestyle='dashed', linewidth=1.5)
    plt.title("Ratio SIBLING 1 - SIBLING 2\n({} cell pairs - included twice (inverse?)".format(int(len(sibling_ratio_list) / 2)))
    plt.xlim(0, 2)
    plt.xlabel("Ratio")
    plt.ylim(-5)
    plt.ylabel("Cell_ID Pairs [#]")

    # Save, show & close:
    plt.savefig(directory + "Hist_Sibling1_vs_Sibling2_Ratio_All.jpeg", bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()


PlotParentChildCCTDiff("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt", show=True, print_stats=True)
print ("\nHistograms plotted in {} mins".format(round((time.process_time() - start_time) / 60, 2)))
