#TODO: Calculate density vs CCT correlation coefficients

import itertools
import numpy as np
import matplotlib.pyplot as plt

def CorrelationDenCCT(density_span="one_quarter", show=False):
    """ Function to calculate correlation coefficients between CCT and density at certain timepoints of cell's life:

    Args:
        density_span (int) -> point of cell's life when calculating: ('8' for "birth", '9' for "one_quarter",
                                        '10' for "half_way", '11' for "three_quarters", '12' for "mitosis")
    Return:
        List of correlation coefficients. Len = 4 ([0] = gen_1, [1] = gen_2, [2] = gen_3, [3] = gen_merged)
        Plot of CCT versus density.

    """

    # Define what a density_span is:
    column = ["birth", "one_quarter", "half_way", "three_quarters", "mitosis"].index(density_span) + 8
    density_file = "/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_merged_density.txt"

    cct = [[] for _ in range(3)]
    den = [[] for _ in range(3)]

    for line in open(density_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Cell_ID-posX-date":
            gen = int(line[5]) - 1              # -1 because counts from 0
            cct[gen].append(float(line[4]))
            den[gen].append(float(line[column]))

    for sub_cct, sub_den in zip(cct, den):
        plt.scatter(x=sub_cct, y=sub_den, alpha=0.5)

    plt.title("Doubling Time vs. Density at {} through cell's lifetime".format(density_span))
    plt.xlabel("Cell Cycle Duration [hours]")
    plt.ylabel("Cell Density [μm-2]")
    plt.ylim(0, 0.002)

    if show is True:
        plt.show()
    plt.close()

    # Gen1, Gen2, Gen3, GenTotal:
    coe = [[] for _ in range(4)]
    coe[0] = np.corrcoef(x=cct[0], y=den[0])[0][1]
    coe[1] = np.corrcoef(x=cct[1], y=den[1])[0][1]
    coe[2] = np.corrcoef(x=cct[2], y=den[2])[0][1]
    coe[3] = np.corrcoef(x=list(itertools.chain.from_iterable(cct)), y=list(itertools.chain.from_iterable(den)))[0][1]

    print ("Correlation Coefficient across all generations, density_span = {}: {}\n\t"
           "Generation #1: {}\n\tGeneration #2: {}\n\tGeneration #3: {}\n\t"
           .format(density_span, coe[3], coe[0], coe[1], coe[2]))

    return coe
