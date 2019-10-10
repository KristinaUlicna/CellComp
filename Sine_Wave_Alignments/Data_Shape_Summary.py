import numpy as np
import matplotlib.pyplot as plt
from itertools import chain


def CharacteriseDataShape(file, limit_low=10.00, limit_high=26.00, show=False, print_stats=False):
    """ Plots the stats & shape of the data.

    :param file:    (string)    -> absolute path into the "generation_X_families.txt" file
    :return:        (list)      -> collection of all CCT (floats) within specified range

    """

    gens = int(file.split("_families.txt")[0][-1])
    cct_gens = [[] for _ in range(gens)]
    counter = 0

    if show is True:
        fig = plt.figure(figsize=(5,10))
        ax = fig.add_subplot(111)       # the big subplot
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
        ax.set_ylabel("Cell Cycle Duration [hours]")
        ax.set_title("Data Distribution per {}-Generational Family; phase = 0".format(gens))

        fig.tight_layout()
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)

    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Gen_1" and line[0] != "Cell_ID":

            # Generate the data for Y-axis which are just the cell cycle durations:
            if gens == 2:
                y_data = np.array([float(line[1]), float(line[4])])
            if gens == 3:
                y_data = np.array([float(line[1]), float(line[4]), float(line[7])])

            # Make sure only data within the limit range are included:
            if not all(value > limit_low and value < limit_high for value in y_data):
                continue
            else:
                counter += 1
                for index in range(gens):
                    cct_gens[index].append(y_data[index])

            # X-axis starts at 'phase' (=unknown) & adds the Y-time points:
            phase = 0.0  # phase = horizontal shift of all my points (not the sine wave, defined as 'shift_h')
            x_data = [phase]
            for cct in y_data:
                phase += cct
                x_data.append(phase)
            x_data.pop(-1)
            x_data = np.array(x_data)

            if show is True:
                ax1.scatter(x=x_data, y=y_data)

    if show is True:
        ax1.set_xlim(-2, 42)
        ax1.set_ylim(limit_low - 2, limit_high + 2)
        ax1.set_xlabel("Time [hours]")
        ax1.set_ylabel("Data Shape")
        ax1.yaxis.set_label_position("right")
        ax1.set_ylim(10, 28)

        ax2.boxplot(cct_gens)
        ax2.set_ylabel("Cell Cycle Duration [hours]")
        ax2.set_xlabel("Generation #")
        ax2.set_ylabel("Median")
        ax2.yaxis.set_label_position("right")
        ax2.set_ylim(10, 28)
        ax2.set_xlim(0.5, 4.0)


        x = [1, 2]
        if gens == 3:
            x = [1, 2, 3]
        ax3.errorbar(x=x, y=[np.mean(i) for i in cct_gens], yerr=[np.std(i) for i in cct_gens], fmt="bo",
                        capsize=4.0, capthick=2.0)
        ax3.set_xlabel("Generation #")
        ax3.set_xticks(x)
        ax3.set_ylabel("Mean ± Std.")
        ax3.yaxis.set_label_position("right")
        ax3.set_ylim(10, 28)
        ax3.set_xlim(0.5, 4.0)

        plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Gen_{}_DataShape.jpeg".format(gens),
                    bbox_inches="tight")
        plt.show()
        plt.close()

    if print_stats is True:
        print("\nFamilies processed for analysis: {}".format(counter))
        print("Families data for {} generations: {}".format(gens, cct_gens))
        print("Generational CCT: (restricted to only include CCTs between {} - {} hours)\n\tmin = {}\tmax = {}"
                .format(limit_low, limit_high, min(chain.from_iterable(cct_gens)), max(chain.from_iterable(cct_gens))))

    for i in range(len(cct_gens)):
        mn = np.mean(cct_gens[i])
        sd = np.std(cct_gens[i])
        md = np.median(cct_gens[i])
        print ("Gen #{}: Mean = {}, St.dev = {}, Median = {}".format(i + 1, mn, sd, md))

    return cct_gens

"""
for i in [3, 2]:
    file = "/Users/kristinaulicna/Documents/Rotation_2/generation_{}_families.txt".format(i)
    cct_gens = CharacteriseDataShape(file=file, show=True, print_stats=True)
"""

file = "/Users/kristinaulicna/Documents/Rotation_2/generation_2_families.txt"
cct_gens = CharacteriseDataShape(file=file, show=True, print_stats=True)
print (cct_gens)
