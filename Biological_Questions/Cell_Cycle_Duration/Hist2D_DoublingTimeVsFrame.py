import matplotlib.pyplot as plt

def Hist2dOscillations(file, span):
    """ Function to plot 2D hist of cell cycle time [hours] according to certain frame value (=span).
        Histogram visualises cells irrespective of generations.

    when cells appear, half-way and when cells cease irrespective of their generation

    Args:
        file (string) ->    full directory to 'cellIDdetails_merged.txt' (can also be 'cellIDdetails_merged_density.txt')
        span (string) ->    "birth", "one_quarter", "half_way", "three_quarters", "mitosis"
                            = the frame accroding to which we want to categorize the cell's doubling time

    Return:
        None.
        Plots the histogram and visualises it in SciView.

    Notes:
        Formula to calculate the absolute frame of appearance at each span point:
                ((en_frame - st_frame) / 4 * span_index) + st_frame = 'value'
    """

    x_axis = []
    y_axis = []

    span_list = ["birth", "one_quarter", "half_way", "three_quarters", "mitosis"]
    color_list = [plt.cm.Reds, plt.cm.Blues, plt.cm.Greens, plt.cm.Oranges, plt.cm.Purples]
    index = span_list.index(span)

    counter = 0
    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Cell_ID-posX-date":
            if float(line[4]) < 10.0:
                counter += 1
            formula = ((int(line[2]) - int(line[1])) / 4 * index) + int(line[1])
            x_axis.append(formula)
            y_axis.append(float(line[4]))

    print (min(x_axis))
    print (max(x_axis))
    print (min(y_axis))
    print (max(y_axis))
    print (counter)
    print ()

    plt.hist2d(x=x_axis, y=y_axis, bins=(150, 24), cmap=color_list[index])
    plt.xlim((150, 1250))
    plt.ylim(10, 35)
    plt.colorbar()
    plt.title("Oscillations depending on the {} real-time frame?\nIrrespective of generation!".format(span))
    plt.xlabel("Frame #")
    plt.ylabel("CCT [hours]")

    # Save, visualise & close the figure:
    directory = file.split("/")[:-1]
    directory = "/".join(directory)
    plt.savefig(directory + "/Hist2D_Oscillations_{}_{}.jpeg".format(index, span), bbox_inches="tight")
    plt.show()
    plt.close()


file = "/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_merged.txt"
for span in ["birth", "one_quarter", "half_way", "three_quarters", "mitosis"]:
    Hist2dOscillations(file=file, span=span)