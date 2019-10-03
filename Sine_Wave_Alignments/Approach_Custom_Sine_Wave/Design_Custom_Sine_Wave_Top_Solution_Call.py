# TODO: Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
#       and align families to minimize loss across the entire dataset - plot the best fit!

from Sine_Wave_Alignments.Approach_Custom_Sine_Wave.Design_Custom_Sine_Wave_Top_Solution_Function import DesignCustomSineWave


# Call the function:
file = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"

amp, per, shift_v = 4.6, 11.7, 17.7
print ("Calculating for amp = {}, per = {}, shift_v = {}".format(amp, per, shift_v))
best_model_mse = DesignCustomSineWave(file=file, amp=amp, per=per, shift_h=0, shift_v=shift_v)

