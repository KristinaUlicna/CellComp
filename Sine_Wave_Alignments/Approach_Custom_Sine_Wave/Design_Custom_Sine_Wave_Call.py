# TODO: Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
#       and align families to minimize loss across the entire dataset - plot the best fit!

import numpy as np
from Sine_Wave_Alignments.Approach_Custom_Sine_Wave.Design_Custom_Sine_Wave_Function import DesignCustomSineWave


# Call the function:
file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/generation_3_families.txt"

top_mse = 1000000
top_params = []

for amp in np.linspace(2, 12, 100 + 1):
    for per in np.linspace(6, 42, 360 + 1):
        for shift_v in np.linspace(12, 24, 120 + 1):

            if per % 6 == 0 and shift_v % 2 == 0:
                print ("Calculating for amp = {}, per = {}, shift_v = {}".format(amp, per, shift_v))

            best_model_mse = DesignCustomSineWave(file=file, amp=amp, per=per, shift_h=0, shift_v=shift_v)

            if best_model_mse < top_mse:
                top_mse = best_model_mse
                top_params = [amp, per, shift_v]

print ("Top Solution;\n\tMean Squared Error = {}\n\tParameters = {}".format(top_mse, top_params))
