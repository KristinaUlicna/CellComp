# TODO: Merge data? Download a few from TeamViewer.
# For now, only compare 2 datafiles (ver0 and ver4).
# TODO: Learn how to do a t-test!

import os
import sys
sys.path.append("../")

from scipy import stats
from Cell_Cycle_Duration.Plot_CC_Duration_Hist import CreateGenerationList


# Call the function & import the generation_list per each file:
large_list = []
directory = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracker_Updates_XML_Files/"
for ver_folder in sorted(os.listdir(directory)):        # !!! sorted() so that it processes folders from first to last!
    if ver_folder != ".DS_Store":
        file = directory + ver_folder + "/cellIDinfo_{}.txt".format(ver_folder)
        generation_list = CreateGenerationList(txt_file=file, print_stats=False)
        large_list.append(generation_list)

print ("THESE ARE _SORTED.TXT FILES, NOT FILTERED. THAT'S WHY SO MANY CELLS!")
print ("Large List: len {} -> {}".format(len(large_list), large_list))



# ----- OPTION : Run independent t-test
# t, p = stats.ttest_ind(array_1, array_2)      # ind = two independent samples' t-test, no need to convert to np array
# print("t = {}".format(t))
# print("p = {}".format(p))


# ----- OPTION : Run ANOVA for each generation:
# (from https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html)
# TODO: This is hard-coded, do soft-coding instead!

_, p_value = stats.f_oneway(large_list[0][0], large_list[1][0], large_list[2][0], large_list[3][0], large_list[4][0])

print ("ANOVA Generation #1 -> p-value: {}".format(float(p_value)))
print ("Are the data significantly different?"
       "\n\tns (P > 0.05) : {}\n\t* (P ≤ 0.05): {}\n\t** (P ≤ 0.01) : {}\n\t*** (P ≤ 0.001) : {}\n\t**** (P ≤ 0.0001) : {}" \
            .format(p_value >= 0.05, p_value <= 0.05, p_value <= 0.01, p_value <= 0.001, p_value <= 0.0001))
