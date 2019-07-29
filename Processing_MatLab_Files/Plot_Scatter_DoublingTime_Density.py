# TODO: Plot scatter plot where x = CCT and y = density at all 5 stages of the cell cycle:

import matplotlib.pyplot as plt
merged_density_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged_density.txt"

def GetGenerationDataforScatter(generation, span):
    """
    Args:
        generation (int)    ->
        span (int)          -> a value of an index for that particular range of densities
                                ('8' for "birth", '9' for "one_quarter", '10' for "half_way",
                                 '11' for "three_quarters", '12' for "mitosis")
    #TODO: Add option for span!
    :param generation:
    :return:
    """

    duration = []
    density = []
    for line in open(merged_density_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Cell_ID-posX-date":
            if int(line[5]) == generation:
                duration.append(float(line[4]))
                density.append(float(line[span]))
    return duration, density


for span in [8, 9, 10, 11, 12]:
    for generation in [1, 2, 3]:
        duration, density = GetGenerationDataforScatter(generation=generation, span=span)
        plt.scatter(x=duration, y=density, alpha=0.5, label="Generation #{}".format(generation))
        plt.title("Doubling Time vs. Density ({}) through cell cycle\ndata from 'cellIDdetails_merged_density.txt'"
                  .format(span))
        plt.xlabel("Cell Cycle Duration [hours]")
        plt.ylabel("Cell Density [units?]")
        plt.xlim(15, 25)
        plt.ylim(0, 0.002)
        plt.legend()
    # Visualise and save the figure:
    plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Scatter_DoublingTimeVsDensitySpan{}_Zoom.jpeg"
                .format(span), bbox_inches="tight")
    plt.show()
    plt.close()