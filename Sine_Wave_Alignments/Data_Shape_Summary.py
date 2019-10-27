import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

def PrintDataSummary(file):
    """

    :param file:
    :return:
    """
    gens_total = file.split("_families.txt")[0][-1]
    counter = 0
    cct_gens = [[] for i in range(3)]
    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == 'Gen_1' or line[0] == 'Cell_ID':
            continue

        # Condition to only include families which take 12.00 < cct < 24.00 hours to divide:
        if len(line) <= 6:
            cct = float(line[1]), float(line[4])
            if cct[0] > 12.00 and cct[0] < 24.00:
                if cct[1] > 12.00 and cct[1] < 24.00:
                    counter += 1
                    for index in range(2):
                        cct_gens[index].append(cct[index])
        else:
            cct = float(line[1]), float(line[4]), float(line[7])
            if cct[0] > 12.00 and cct[0] < 24.00:
                if cct[1] > 12.00 and cct[1] < 24.00:
                    if cct[2] > 12.00 and cct[2] < 24.00:
                        counter += 1
                        for index in range(3):
                            cct_gens[index].append(cct[index])

    minimum = min(chain.from_iterable(cct_gens))
    maximum = max(chain.from_iterable(cct_gens))

    print ("\nFamilies processed for analysis: {}".format(counter))
    print ("Families data for {} generations: {}".format(gens_total, cct_gens))
    print ("Generational CCT: (restricted to only include CCTs between 12.00 - 24.00 hours)"
           "\n\tmin = {}\tmax = {}".format(minimum, maximum))


def PlotDataShape(file):
    """

    :param file:
    :return:
    """

    gens_total = file.split("_families.txt")[0][-1]

    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Gen_1" and line[0] != "Cell_ID":
            line = [float(value) if "." in value else int(value) for value in line]

            # Generate the data for Y-axis which are just the cell cycle durations:
            if len(line) <= 6:
                lineage = [line[0:3], line[3:6]]
                y_data = np.array([lineage[0][1], lineage[1][1]])
            else:
                lineage = [line[0:3], line[3:6], line[6:9]]
                y_data = np.array([lineage[0][1], lineage[1][1], lineage[2][1]])

            # X-axis starts at 'phase' (=unknown) & adds the Y-time points:
            phase = 0.0  # phase = horizontal shift of all my points (not the sine wave, defined as 'shift_h')
            x_data = [phase]
            for cct in y_data:
                phase += cct
                x_data.append(phase)
            x_data.pop(-1)
            x_data = np.array(x_data)

            plt.scatter(x=x_data, y=y_data)

    plt.title("Data Distribution per {}-Generational Family; phase = 0".format(gens_total))
    plt.xlabel("Time [hours]")
    plt.ylabel("Cell Cycle Duration [hours]")
    plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Gen_{}_DataShape.jpeg".format(gens_total), bbox_inches="tight")
    plt.show()
    plt.close()


file_3_gen = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"
PrintDataSummary(file=file_3_gen)
PlotDataShape(file=file_3_gen)

file_2_gen = "/Users/kristinaulicna/Documents/Rotation_2/generation_2_families.txt"
PrintDataSummary(file=file_2_gen)
PlotDataShape(file=file_2_gen)

