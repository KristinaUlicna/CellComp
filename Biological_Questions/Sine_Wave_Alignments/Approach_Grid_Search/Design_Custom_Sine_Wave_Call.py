# "Grid Search" Approach:
#       Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
#       and align families to minimize loss across the entire dataset - plot the best fit!

import numpy as np
from Biological_Questions.Sine_Wave_Alignments.Approach_Grid_Search \
    import DesignCustomSineWave, PrepareFamilyList

file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/generation_2_families.txt"
family_list = PrepareFamilyList(file=file, how_many_gen=2)

"""
# Call the function for single sine wave with pre-defined hyperparameters:
amp, per, shift_v = 4.59, 11.75, 17.71
print ("Calculating for amp = {}, per = {}, shift_v = {}".format(amp, per, shift_v))
best_model_mse = DesignCustomSineWave(family_list=family_list, how_many_gen=3, amp=amp, per=per, shift_h=0, shift_v=shift_v,
                                      show=True, print_phase_mse=False)
print ("\nSolution:\tMean Squared Error = {}\tParameters = {}".format(best_model_mse, [amp, per, shift_v]))
"""


# Call the function for a range of parameter combinations & print top 10 best solutions!:
top_mse = [1000000 for _ in range(10)]
top_params = [[] for _ in range(10)]

combinations = 0
"""
for amp in np.linspace(4.4, 4.6, 2 + 1):
    for per in np.linspace(18.8, 19.2, 4 + 1):
        for shift_v in np.linspace(18.3, 18.7, 4 + 1):
"""

result_mse_list = []

for amp in [4.6]:
    for per in [19.2]:
        for shift_v in np.linspace(12.0, 24.0, 121):

            combinations += 1
            if shift_v % 2 == 0:
                print ("Calculating for amp = {}, per = {}, shift_v = {}".format(amp, per, shift_v))

            best_model_mse = DesignCustomSineWave(family_list=family_list, how_many_gen=2,
                                                  amp=amp, per=per, shift_h=0, shift_v=shift_v)

            result_mse_list.append(best_model_mse)

            if best_model_mse < top_mse[0]:
                for i in range(8, -1, -1):      # reversed order
                    top_mse[i+1] = top_mse[i]
                    top_params[i+1] = top_params[i]
                top_mse[0] = best_model_mse
                top_params[0] = [amp, per, shift_v]


print ("Top 10 Solutions from {} combinations\n".format(combinations))
for counter, (mse, params) in enumerate(zip(top_mse, top_params)):
    print ("\tTop #{}: \tMean Squared Error = {}\tParameters = {}".format(counter + 1, mse, params))


file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE_Summary.txt"
file = open(file, "a+")
file.write("Amp = 2.0, 12.0, 101 (iter)\tPer = 19.2 (fixed)\tShift_v = 18.6 (fixed)\t\n")
for item in result_mse_list:
    file.write(str(item) + " ")
file.write("\n")
file.close()

print (result_mse_list)
