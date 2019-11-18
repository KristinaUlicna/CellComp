# TODO: Plot cumulative histogram that will show :
# predicted distribution (thick black line)
# and 18 individual movies (thinner lines).

import sys
sys.path.append("../")

import numpy as np
import matplotlib.pyplot as plt
from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths
from Biological_Questions.Cell_Cycle_Duration.Plot_CC_Duration_Hist import PlotHistGenerationCCT

# TODO: What's the point of having this function separate
# if the script 'Plot_CC_Duration_Hist' has a function to do the same?

def PlotHistCumul_AllMovies(exp_type="MDCK_WT_Pure", generation=1, show=False):
    """ Identify outlier movies by plotting an CDF.
        Plots CDF = cumulative density function.
        Tutorial: https://matplotlib.org/gallery/statistics/histogram_cumulative.html
    """

    # Extract, analyse & plot merged data first (zorder = high -> to ensure it will be on top):
    directory = "/Volumes/lowegrp/Data/Kristina/{}/".format(exp_type)
    merged_file = directory + "cellIDdetails_merged.txt"
    generation_list = PlotHistGenerationCCT(txt_file=merged_file).CreateGenerationList(print_stats=False)
    gen = generation_list[generation-1]
    merged_mean = round(np.mean(gen), 2)
    merged_std = round(np.std(gen), 2)

    # Plot cumulative hist of merged data:
    n_bins = 50
    plt.figure(figsize=(8.5, 6))
    plt.hist(gen, bins=n_bins, density=True, histtype='step', cumulative=True, linewidth=3.0, color='black',
             label='MERGED DATA\ncellIDs = {}'.format(len(gen)), zorder=20)
    plt.axvline(merged_mean, alpha=0.5, color='grey', zorder=1, linestyle='dashed', linewidth=2.0)
    plt.axvspan(merged_mean - merged_std, merged_mean + merged_std, alpha=0.3, color='grey', zorder=1,
                label='MERGED DATA\nMean ± St.Dev\n{} ± {}'.format(merged_mean, merged_std))

    # Now add individual movies to the plot:
    _, txt_file_list = GetMovieFilesPaths(exp_type=exp_type)

    for file in sorted(txt_file_list):
        filtered_file = file.replace("raw", "filtered")
        file = file.split("/")
        file_generation_list = PlotHistGenerationCCT(txt_file=filtered_file).CreateGenerationList(print_stats=False)
        if len(file_generation_list) >= generation:       # to make sure that index is not out of range in the list
            file_gen = file_generation_list[generation-1]
            plt.hist(file_gen, bins=n_bins, density=True, histtype='step', cumulative=True, linewidth=1.5,
                     label='{}-{}\ncellIDs = {}'.format(file[-4], file[-3], len(file_gen)))

    # Tidy up the figure:
    plt.title("Cumulative step histograms:\nGeneration #{} - Merged data vs. {} '{}' movies"
              .format(generation, len(txt_file_list), exp_type))
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)
    plt.ylabel('Likelihood of occurrence')
    plt.xlabel('Cell Cycle Duration [hours]')
    plt.xticks(list(range(0, n_bins + 2, 2)))
    plt.xlim(0 - n_bins / 20, n_bins + n_bins / 20)  # 5% ± the min & max point
    plt.ylim(-0.1, 1.1)

    # Save, show & close:
    plt.savefig(directory + 'Hist_Cumulative_CCT_Gen-{}_All-Movies.jpeg'.format(generation), bbox_inches="tight")
    if show is True:
        plt.show()
    plt.close()
