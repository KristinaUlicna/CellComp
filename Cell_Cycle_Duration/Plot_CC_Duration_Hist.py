import matplotlib.pyplot as plt
import math


def CreateGenerationList(txt_file, print_stats=True):
    """ Plot multiple histograms per generation into one figure.
        Use 'cellIDdetails_filtered.txt' (preferred)
        or 'cellIDdetails_sorted.txt' as input file.

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
    if print_stats is True:
        print ("Txt_file processed:\t{}".format(txt_file))
        gen_list = []
        for gen in generation_list:
            gen_list.append(len(gen))
        print ("Generations total = {}; Length of sub-lists = {}; Whole gen list = {}" \
               .format(len(generation_list), gen_list, generation_list))

    return generation_list


def PlotHistGenerationCCT(txt_file, show=False):
    """ Plots a figure with overlapping histograms, each depicting the distributions
        of cell cycle durations [hours] per single generation. """

    # Call the previous function:
    generation_list = CreateGenerationList(txt_file=txt_file)
    file_type = "filtered" if "filtered" in txt_file else "sorted"
    directory = "/".join(txt_file.split("/")[:-1]) + "/"
    # TODO: Create new folder for CCT analysis

    # Some vectors for plotting:
    bins = int(math.ceil(max(sum(generation_list, [])) / 5.0)) * 5
    bin_edges = list(range(0, bins + 1, 1))
    bin_xticks = list(range(0, bins + 2, 2))

    # Plot the 'stacked' histogram:
    for number, gen in enumerate(generation_list):
        a, b, c = plt.hist(gen, bins=bin_edges, edgecolor='black', linewidth=1.0, alpha=0.5, label='Generation {}'.format(number + 1))
    plt.legend()                # change location to "loc='upper left'" if necessary
    plt.title("Generational Cell Cycle Duration (data: cellIDdetails_{}.txt".format(file_type))

    plt.xticks(bin_xticks)
    plt.xlabel("Cell Cycle Duration [hours]")
    plt.ylim((a.max() * -1 / 10))                # y_lim = -10% of max y-axis value
    plt.ylabel("Cell ID count")

    # Save, show & close:
    plt.savefig(directory + 'Hist_Generational_CCT_{}.jpeg'.format(file_type), bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()
