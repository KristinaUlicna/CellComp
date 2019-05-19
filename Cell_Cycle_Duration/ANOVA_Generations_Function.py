# Function that will run an ANOVA on all generations from input directory files:

import os
import sys
sys.path.append("../")

import numpy as np
from scipy import stats
from Cell_Cycle_Duration.Plot_CC_Duration_Hist import CreateGenerationList



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

    # Call the function & import the generation_list per each file:
    large_list = []
    print ("Directory: {}".format(directory))
    for ver_folder in sorted(os.listdir(directory)):  # !!! sorted() so that it processes folders from first to last!
        if ver_folder != ".DS_Store":
            file = directory + ver_folder + "/cellIDinfo_{}.txt".format(ver_folder)
            generation_list = CreateGenerationList(txt_file=file, print_stats=False)
            large_list.append(generation_list)

    print("THESE ARE _SORTED.TXT FILES, NOT FILTERED. THAT'S WHY SO MANY CELLS!")
    print("Large List: len {} -> {}".format(len(large_list), large_list))

    # Understand your large_list:
    for file_order, single_file in enumerate(large_list):
        for gen_order, single_generation in enumerate(single_file):
            print ("File #{} -> Generation #{} -> {}".format(file_order + 1, gen_order + 1, single_generation))

    # Run ANOVA for each generation:
    file_number = len(large_list)
    print ("How many files are we running stats on? \t{}".format(file_number))
    max_gener = 0
    for single_file in large_list:
        if len(single_file) > max_gener:
            max_gener = len(single_file)
    print ("Up to how many generations do we have?  \t{}".format(max_gener))

    def RunAnova(generation):
        """ Select the generation for which you want to run the ANOVA across all files.
            generation (integer)    ->    which generation you want to do it for?
            TODO: Write a while loop to run the thing for.
        """

        # Initiate the lists, I suppose...
        try:
            file_1 = large_list[0][generation - 1]
        except:
            file_1 = []

        try:
            file_2 = large_list[1][generation - 1]
        except:
            file_2 = []

        try:
            file_3 = large_list[2][generation - 1]
        except:
            file_3 = []

        try:
            file_4 = large_list[3][generation - 1]
        except:
            file_4 = []

        try:
            file_5 = large_list[4][generation - 1]
        except:
            file_5 = []

        # Run the ANOVA for the specified generation:
        _, p_value = stats.f_oneway(file_1, file_2, file_3, file_4, file_5)

        print("ANOVA Generation #{} -> p-value: {}".format(generation, float(p_value)))
        print("Are the data significantly different?\n\tns (P > 0.05) : {}\n\t* (P ≤ 0.05): {}"
              "\n\t** (P ≤ 0.01) : {}\n\t*** (P ≤ 0.001) : {}\n\t**** (P ≤ 0.0001) : {}" \
              .format(p_value >= 0.05, p_value <= 0.05, p_value <= 0.01, p_value <= 0.001, p_value <= 0.0001))

    generation = 1
    while generation <= max_gener:          #TODO: Smaller or smaller/equal?
        RunAnova(generation=generation)
        generation += 1


GenerationsForANOVA("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracker_Updates_XML_Files/")