# Function that will run an ANOVA on all generations from input directory files:

import sys
sys.path.append("../")

from scipy import stats
from Biological_Questions.Cell_Cycle_Duration.Plot_CC_Duration_Hist import PlotHistGenerationCCT
from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


def GenerationsForANOVA(exp_type="MDCK_WT_Pure"):
    """ Function that runs an ANOVA statistical test on all generations from input directory files.

    Args:
        exp_type (string)  ->  folder to be iterated through to extract files from to compare generations.

    Return:
        None.
        Prints a lot of stats.

    Notes:
        ANOVA Scipy tutorial at: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html

    """

    # Call the function & import the generation_list per each file (server):
    _, txt_file_list = GetMovieFilesPaths(exp_type=exp_type)

    large_list = []
    for file in sorted(txt_file_list):
        file = file.replace("raw", "filtered")
        #print("File: {}".format(file))
        call = PlotHistGenerationCCT(txt_file=file)
        generation_list = call.CreateGenerationList(print_stats=True)
        large_list.append(generation_list)
    print("\nLarge List: len = {} -> {}".format(len(large_list), large_list))

    # Understand your large_list:
    files = list(range(1, 22))
    gener = [0] * len(txt_file_list)
    for file_order, single_file in enumerate(large_list):
        for gen_order, single_generation in enumerate(single_file):
            print ("File #{} -> Generation #{} -> {}".format(file_order + 1, gen_order + 1, single_generation))
            gener[file_order] = gen_order + 1
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
                                    large_list[5][generation - 1],
                                    large_list[6][generation - 1],
                                    large_list[7][generation - 1],
                                    large_list[8][generation - 1],
                                    large_list[9][generation - 1],
                                    large_list[10][generation - 1],
                                    large_list[11][generation - 1],
                                    large_list[12][generation - 1],
                                    large_list[13][generation - 1],
                                    large_list[14][generation - 1],
                                    large_list[15][generation - 1],
                                    large_list[16][generation - 1],
                                    large_list[17][generation - 1])

        print("\nANOVA Generation #{} -> p-value: {}".format(generation, float(p_value)))
        print("Are the data significantly different?\n\tns (P > 0.05) : {}\n\t* (P ≤ 0.05): {}"
              "\n\t** (P ≤ 0.01) : {}\n\t*** (P ≤ 0.001) : {}\n\t**** (P ≤ 0.0001) : {}" \
              .format(p_value >= 0.05, p_value <= 0.05, p_value <= 0.01, p_value <= 0.001, p_value <= 0.0001))

    # For now, just run the stats for generation #1:
    RunAnova(generation=1)

    # If you had more generations:
    #generation = 1
    #while generation <= max(gener):
    #    RunAnova(generation=generation)
    #    generation += 1


# Call the function:
GenerationsForANOVA(exp_type="MDCK_WT_Pure")