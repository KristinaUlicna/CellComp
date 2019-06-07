import matplotlib.pyplot as plt
import statistics as stats
import numpy as np
import math
import os

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


class PlotHistGenerationCCT(object):
    """ Try / except if functions are not called in order! """

    def __init__(self, txt_file):

        # Input file / directory folder / saved figure organisation:
        self.txt_file = txt_file
        self.file_type = str(self.txt_file).split("cellIDdetails_")[-1].split(".txt")[0]
        if self.file_type == "merged":
            self.directory = "/".join(self.txt_file.split("/")[:-1]) + "/"
        else:
            self.directory = "/".join(self.txt_file.split("/")[:-1]) + "/cellcycle/"
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)

        # Return vectors from functions:
        self.generation_list = None         # TODO: Call try/except if 1st function is not called!
        self.values_per_bin = None
        self.mean = None
        self.std = None


    def CreateGenerationList(self, print_stats=False):
        """ Plot multiple histograms per generation into one figure.
            Use 'cellIDdetails_filtered.txt' (preferred)
            or 'cellIDdetails_sorted.txt' as input file.

        Args:
            txt_file (string)                       ->    absolute directory to 'cellIDdetails_raw.txt' (use replace option)
            print_stats (boolean, set to False)     ->    show the generation_list stats or not

        Return:
            "pseudo return" - it's a self.variable so no need for returns!

            generation_list (list)  ->   [[16.93, 5.78, 13.40, ...], [16.93, 5.78, 13.40, ...], []]
                                          |-> generation #1          |-> generation #2            |-> file
        """

        # Categorize CCT according to the generations:
        self.generation_list = [[]]
        for line in open(self.txt_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date":
                continue
            gen = int(line[5])
            cct = float(line[4])               # cell cycle duration in hours
            if gen > len(self.generation_list):     # append by as many empty lists as are missing!
                self.generation_list.append(([] * (gen - len(self.generation_list))))
            self.generation_list[gen-1].append(cct)

        # Calculate the mean & st.dev for each generation:
        self.mean = [[] for _ in range(len(self.generation_list))]
        self.std = [[] for _ in range(len(self.generation_list))]

        for number, gen in enumerate(self.generation_list):
            if len(gen) >= 2:
                self.mean[number] = round(stats.mean(gen), 2)
                self.std[number] = round(stats.stdev(gen), 2)
            elif len(gen) == 1:
                self.mean[number] = gen
                self.std[number] = 0
            else:
                self.mean[number] = 0
                self.std[number] = 0

        # Print summary:
        if print_stats is True:
            print ("Txt_file processed:\t{}".format(self.txt_file))
            print ("Whole generation list:\t{}".format(self.generation_list))
            for order, gen in enumerate(self.generation_list):
                print ("Gen #{}\tlength = {}\tmean = {}; st.dev. = {}\tgen-sublist: {}"
                       .format(order, len(gen), self.mean[order], self.std[order], gen))


    def PlotHistSimple(self, show=False):
        """ Plots a figure with overlapping histograms, each depicting the distributions
            of cell cycle durations [hours] per single generation.
        Args:
            txt_file (string)       -> file to be analysed
            show (boolean)          -> whether to visualise the figure in SciView or not

        Return:
            Plot visualised (optional) & saved in the specified directory.

        Notes:
            TODO: Play with the 'density' and 'weights' parameters of plt.hist option.
            TODO: you should be able to plot the normalised histogram easily (no need for separate function)
        """

        # Make vectors for plotting:
        if len(self.generation_list[0]) > 2:
            bins = int(math.ceil(max(sum(self.generation_list, [])) / 5.0)) * 5
        else:
            bins = 1
        bin_edges = list(range(0, bins + 1, 1))
        bin_xticks = list(range(0, bins + 2, 2))

        # Plot the 'stacked' histogram:
        self.values_per_bin = [[] for _ in range(len(self.generation_list))]

        for number, gen in enumerate(self.generation_list):
            self.values_per_bin[number], _, _ = plt.hist(x=gen, bins=bin_edges, edgecolor='black', linewidth=1.0, alpha=0.5,
                                                label='Generation #{}\ncellIDs = {}'.format(number + 1, len(gen)))
            if number == 0:
                # One st.dev away from the mean:
                plt.axvline(self.mean[number], color='gold', linestyle='dashed', linewidth=2.0, label= \
                            "Generation #{};\nmean ± st.dev\n({} ± {})" \
                            .format(number + 1, self.mean[number], self.std[number]))
                plt.axvline(self.mean[number] + self.std[number], color='gold', linestyle='dashed', linewidth=1.0)
                plt.axvline(self.mean[number] - self.std[number], color='gold', linestyle='dashed', linewidth=1.0)

                # Two st.devs away from the mean:
                plt.axvline(x=self.mean[number] + (2*self.std[number]), color='gold', linestyle='dashed', linewidth=1.0, alpha=0.6)
                plt.axvline(x=self.mean[number] - (2*self.std[number]), color='gold', linestyle='dashed', linewidth=1.0, alpha=0.6)

                # Fill between upper & lower boundary for outliers (mean-1*std & mean-2*std):
                plt.axvspan(self.mean[number] - (2*self.std[number]), self.mean[number] - (1*self.std[number]),
                            alpha=0.3, color='plum', zorder=1, label='Left-skewed outliers')

        plt.title("Generational Cell Cycle Duration (cellIDdetails_{}.txt)".format(self.file_type))
        plt.legend()    # change location to "loc='upper left'" if necessary
        plt.xticks(bin_xticks)
        plt.xlabel("Cell Cycle Duration [hours]")
        plt.ylim(self.values_per_bin[0].max() * -1 / 20)       # y_lim = -5% of max y-axis value from Gen #1
        plt.ylabel("Cell ID count")

        # Save, show & close:
        plt.savefig(self.directory + 'Hist_Generational_CCT_{}.jpeg'.format(self.file_type), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotHistNormalisedTOBEFIXED(self, show=False):
        """ Plots normalised BAR PLOT (not histogram!) for generation 1 of the txt file.
            -> normalises the bars to the relative percentage of highest bin value (=1.0)

        Args:
            txt_file (string)       -> file to be analysed (preferrably cellIDdetails_merged.txt)
            show (boolean)          -> whether to visualise the figure in SciView or not

        Return:
            None.
            Plots visualised (optional) & saved in the specified directory.

        Notes:
            TODO: Fix this one!
            TODO: Expand to more than 2 generations when data is available.
        """

        # Convert the array into lists & calculate the percentage against the highest bin:

        values_per_bin = self.values_per_bin
        number_of_bins = [[] for _ in range(len(values_per_bin))]

        for order, array in enumerate(values_per_bin):
            number_of_bins[order] = len(array)
            maximum = array.max()
            values_per_bin[order] = array.tolist()
            values_per_bin[order] = [round(value * 100 / maximum, 2) for value in values_per_bin[order]]
        print(values_per_bin)

        number_of_bins = list(range(1, len(values_per_bin[0]) + 1, 1))
        print (len(values_per_bin[0]))
        print (number_of_bins)

        for values in values_per_bin:
            plt.bar(x=number_of_bins, height=values)
        plt.show()
        plt.close()


        """
        # Loop through first two generations (at the moment, there is not enough data available for gen 2+)
        for gen in [1, 2]:
            try:
                values_per_bin = self.values_per_bin[gen - 1]
            except:
                print("Warning, not enough data to normalise generation {}!".format(gen))
                continue
            if gen == 1:
                color = "dodgerblue"
                alpha = 0.5
            elif gen == 2:
                color = "orange"
                alpha = 0.5
            else:
                print("Warning, not enough data to normalise generation {}+!".format(gen))
                break

            # What are you normalising against?
            values_per_bin = [int(item) for item in values_per_bin]
            sum_cellIDs = sum(list(values_per_bin))
            norm_100 = max(list(values_per_bin))

            # Rule of three:    norm_100 is 100%, therefore values_per_bin[index] is x%:
            norm_x_axis = [item + 0.5 for item in list(range(0, len(values_per_bin)))]
            norm_y_axis = [round(item * 100 / norm_100, 2) for item in values_per_bin]

            # Plot the thing:
            plt.bar(x=norm_x_axis, height=norm_y_axis, color=color, edgecolor='black', linewidth=1.0, alpha=alpha,
                    label='Generation #{}\ncellIDs = {}'.format(gen, sum_cellIDs))
            plt.axvline(self.mean[gen - 1], color=color, linestyle='dashed', linewidth=2.0, label= \
                "Generation #{};\nmean ± st.dev\n({} ± {})".format(gen, self.mean[gen - 1], self.std[gen - 1]))
            plt.axvline(self.mean[gen - 1] + self.std[gen - 1], color=color, linestyle='dashed', linewidth=1.0)
            plt.axvline(self.mean[gen - 1] - self.std[gen - 1], color=color, linestyle='dashed', linewidth=1.0)

            # Tidy up the figure:
            plt.legend(loc='upper right')
            plt.title(
                "Normalised histogram for {} generations ({})".format(gen, "cellIDdetails_" + self.file_type + ".txt"))
            plt.xticks(list(range(0, len(values_per_bin) + 1, 2)))
            plt.xlabel("Cell Cycle Duration [hours]")
            plt.ylim(-5, 105)
            plt.ylabel("Total CellID Count [%]")

        # Save, show & close:
        plt.savefig(self.directory + 'Hist_Generational_CCT_{}_Normalised.jpeg'.format(self.file_type),
                    bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()
        """

    def PlotHistNormalised(self, show=False):
        """ Plots normalised BAR PLOT (not histogram!) for generation 1 of the txt file.
            -> normalises the bars to the relative percentage of highest bin value (=1.0)

        Args:
            txt_file (string)       -> file to be analysed (preferrably cellIDdetails_merged.txt)
            show (boolean)          -> whether to visualise the figure in SciView or not

        Return:
            None.
            Plots visualised (optional) & saved in the specified directory.

        Notes:
            TODO: Expand to more than 2 generations when data is available.
        """

        # Loop through first two generations (at the moment, there is not enough data available for gen 2+)
        for gen in [1, 2, 3]:
            try:
                values_per_bin = self.values_per_bin[gen - 1]
            except:
                print ("Warning, not enough data to normalise generation {}!".format(gen))
                continue
            if gen == 1:
                color = "dodgerblue"
                alpha = 0.5
            elif gen == 2:
                color = "orange"
                alpha = 0.5
            else:
                print ("Warning, not enough data to normalise generation {}+!".format(gen))
                break

            # What are you normalising against?
            values_per_bin = [int(item) for item in values_per_bin]
            sum_cellIDs = sum(list(values_per_bin))
            norm_100 = max(list(values_per_bin))

            # Rule of three:    norm_100 is 100%, therefore values_per_bin[index] is x%:
            norm_x_axis = [item + 0.5 for item in list(range(0, len(values_per_bin)))]
            norm_y_axis = [round(item * 100 / norm_100, 2) for item in values_per_bin]

            # Plot the thing:
            plt.bar(x=norm_x_axis, height=norm_y_axis, color=color, edgecolor='black', linewidth=1.0, alpha=0.5,
                    label='Generation #{}\ncellIDs = {}'.format(gen, sum_cellIDs))
            plt.axvline(self.mean[gen-1], color=color, linestyle='dashed', linewidth=2.0, label= \
                        "Generation #{};\nmean ± st.dev\n({} ± {})".format(gen, self.mean[gen-1], self.std[gen-1]))
            plt.axvline(self.mean[gen-1] + self.std[gen-1], color=color, linestyle='dashed', linewidth=1.0)
            plt.axvline(self.mean[gen-1] - self.std[gen-1], color=color, linestyle='dashed', linewidth=1.0)

            # Tidy up the figure:
            plt.legend(loc='upper right')
            plt.title("Normalised histogram for {} generations ({})"
                      .format(gen, "cellIDdetails_" + self.file_type + ".txt"))
            plt.xticks(list(range(0, len(values_per_bin) + 1, 2)))
            plt.xlabel("Cell Cycle Duration [hours]")
            plt.ylim(-5, 105)
            plt.ylabel("Total CellID Count [%]")

        # Save, show & close:
        plt.savefig(self.directory + 'Hist_Generational_CCT_{}_Normalised.jpeg'.format(self.file_type), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()


    def PlotHistCumulative(self, show=False):
        """ Plots CDF = cumulative density function.
            Tutorial: https://matplotlib.org/gallery/statistics/histogram_cumulative.html
        """

        n_bins = 50
        color_list = ["dodgerblue", "orange", "green", "red"]
        mean_std_lim = [[-0.1, 0.3], [0.3, 0.7], [0.7, 1.1]]

        # Plot the cumulative histogram
        plt.figure(figsize=(8, 4))
        for number, gen in enumerate(self.generation_list):
            # TODO: Check why it comes back to 0
            plt.hist(gen, bins=n_bins, density=True, histtype='step', cumulative=True, linewidth=2.0,
                        label='Generation #{}\ncellIDs = {}'.format(number + 1, len(gen)))
            if number <= 2:
                plt.axvline(self.mean[number], ymin=mean_std_lim[number][0], ymax=mean_std_lim[number][1],
                            linestyle='dashed', linewidth=2.0, color=color_list[number], alpha=0.5,
                            label="Generation #{};\nmean ± st.dev\n({} ± {})".format(number + 1, self.mean[number], self.std[number]))
                plt.axvline(self.mean[number] + self.std[number], ymin=mean_std_lim[number][0], ymax=mean_std_lim[number][1],
                            color=color_list[number], linestyle='dashed', linewidth=1.0)
                plt.axvline(self.mean[number] - self.std[number], ymin=mean_std_lim[number][0], ymax=mean_std_lim[number][1],
                            color=color_list[number], linestyle='dashed', linewidth=1.0)

        # Tidy up the figure:
        plt.grid(False)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Cumulative step histograms; {}'
                     .format("cellIDdetails_" + self.file_type + ".txt"))
        plt.ylabel('Likelihood of occurrence')
        plt.ylim(-0.1, 1.1)         # divide into thirds: -0.1 to 0.3 | 0.3 to 0.7 | 0.7 to 1.1
        plt.xlabel('Cell Cycle Duration [hours]')
        plt.xticks(list(range(0, n_bins + 2, 2)))
        plt.xlim(0 - n_bins/20, n_bins + n_bins/20)     # 5% ± the min & max point

        # Save, show & close:
        plt.savefig(self.directory + 'Hist_Generational_CCT_{}_Cumulative.jpeg'
                    .format(self.file_type), bbox_inches="tight")
        if show is True:
            plt.show()
        plt.close()
