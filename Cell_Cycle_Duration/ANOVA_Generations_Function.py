# Function that will run an ANOVA on all generations from input directory files:

import os
import sys
sys.path.append("../")

import numpy as np
from scipy import stats
from Cell_Cycle_Duration.Plot_CC_Duration_Hist import CreateGenerationList
from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


def GenerationsForANOVA(directory):
    """ Function that runs an ANOVA statistical test on all generations from input directory files.
    Args:
        directory (string)  ->  folder to be iterated through to extract files to compare generations.

    Return:
        None.
        Prints a lot of stats.

    Notes:
        ANOVA Scipy tutorial at: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html

    """

    # Call the function & import the generation_list per each file (ver0-4):
    """
    large_list = []
    print ("Directory: {}".format(directory))
    for ver_folder in sorted(os.listdir(directory)):  # !!! sorted() so that it processes folders from first to last!
        if ver_folder != ".DS_Store":
            file = directory + ver_folder + "/cellIDinfo_{}.txt".format(ver_folder)
            generation_list = CreateGenerationList(txt_file=file, print_stats=False)
            large_list.append(generation_list)

    print("THESE ARE _SORTED.TXT FILES, NOT FILTERED. THAT'S WHY SO MANY CELLS!")
    print("Large List: len {} -> {}".format(len(large_list), large_list))
    """

    # Call the function & import the generation_list per each file (server):
    _, txt_file_list = GetMovieFilesPaths()

    large_list = []
    for file in sorted(txt_file_list):
        file = file.replace("raw", "filtered")
        #print("File: {}".format(file))
        generation_list = CreateGenerationList(txt_file=file, print_stats=False)
        large_list.append(generation_list)
    print("Large List: len = {} -> {}".format(len(large_list), large_list))

    # Understand your large_list:
    files = list(range(1, 22))
    gener = [0] * 21
    for file_order, single_file in enumerate(large_list):
        for gen_order, single_generation in enumerate(single_file):
            print ("File #{} -> Generation #{} -> {}".format(file_order + 1, gen_order + 1, single_generation))
            gener[file_order] = gen_order+1
    print ("\nNumber of files: {} -> {}".format(max(files), files))
    print ("Generations per file: {} -> {}".format(max(gener), gener))


    def RunAnova(generation):
        """ Select the generation for which you want to run the ANOVA across all files.
            generation (integer)    ->    which generation you want to do it for?
            TODO: Write a while loop to run the thing for.
        """

        # Run the ANOVA on GENERATION 1 only, for now...

        _, p_value = stats.f_oneway(large_list[0][generation - 1],
                                    large_list[1][generation - 1],
                                    large_list[2][generation - 1],
                                    large_list[3][generation - 1],
                                    large_list[4][generation - 1],
                                    #large_list[5][generation - 1],
                                    #large_list[6][generation - 1],
                                    #large_list[7][generation - 1],
                                    large_list[8][generation - 1],
                                    large_list[9][generation - 1],
                                    large_list[10][generation - 1],
                                    large_list[11][generation - 1],
                                    large_list[12][generation - 1],
                                    large_list[13][generation - 1],
                                    large_list[14][generation - 1],
                                    large_list[15][generation - 1],
                                    large_list[16][generation - 1],
                                    large_list[17][generation - 1],
                                    large_list[18][generation - 1],
                                    large_list[19][generation - 1],
                                    large_list[20][generation - 1])

        print("\nANOVA Generation #{} -> p-value: {}".format(generation, float(p_value)))
        print("Are the data significantly different?\n\tns (P > 0.05) : {}\n\t* (P ≤ 0.05): {}"
              "\n\t** (P ≤ 0.01) : {}\n\t*** (P ≤ 0.001) : {}\n\t**** (P ≤ 0.0001) : {}" \
              .format(p_value >= 0.05, p_value <= 0.05, p_value <= 0.01, p_value <= 0.001, p_value <= 0.0001))
    """
    generation = 1
    while generation <= max(gener):          #TODO: Smaller or smaller/equal?
        RunAnova(generation=generation)
        generation += 1
    """
    RunAnova(generation=1)


GenerationsForANOVA("pseudo")