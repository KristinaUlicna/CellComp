# "Grid Search" Approach:
#       Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
#       and align families to minimize loss across the entire dataset - plot the best fit!

import time
import numpy as np
from Biological_Questions.Sine_Wave_Alignments.Approach_Grid_Search.Design_Custom_Sine_Wave_Function_Deprecated \
    import DesignCustomSineWave, PrepareFamilyList


file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/generation_2_families.txt"
family_list = PrepareFamilyList(file=file, how_many_gen=2)


def FindBestSineWaveFit(amp_st = 2.0, amp_en = 12.0,
                        per_st = 6.0, per_en = 42.0,
                        sft_st = 12.0, sft_en = 24.0,
                        increment=0.5, write_file=False,
                        top_solutions=False):

    # Start measuring time:
    start = time.time()

    # Create a list of all possible combinations to iterate through:
    range_amp = np.linspace(amp_st, amp_en, int((amp_en-amp_st)/increment)+1)
    range_per = np.linspace(per_st, per_en, int((per_en-per_st)/increment)+1)
    range_sft = np.linspace(sft_st, sft_en, int((sft_en-sft_st)/increment)+1)

    combos = []
    for amp in range_amp:
        for per in range_per:
            for shift_v in range_sft:
                combos.append([amp, per, shift_v])
    print ("Combos: {}\n".format(len(combos)))

    # Write the specification of that combo list creator (the above for-loop) into a multiline string:
    header_string = ""
    header_string += "combos = []\n"
    header_string += "for amp in np.linspace({}, {}, {}):\n"\
        .format(amp_st, amp_en, int((amp_en-amp_st)/increment)+1)
    header_string += "    for per in np.linspace({}, {}, {}):\n"\
        .format(per_st, per_en, int((per_en-per_st)/increment)+1)
    header_string += "        for shift_v in np.linspace({}, {}, {}):\n"\
        .format(sft_st, sft_en, int((sft_en-sft_st)/increment)+1)
    header_string += "            combos.append([amp, per, shift_v])\n"
    header_string += "print ('Combos: {}'.format(len(combos)))\n\n"

    # Create a txt.file into which you will write you MSE results:
    if write_file is True:
        mse_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE.txt"
        mse_file = open(mse_file, "w")
        mse_file.write(header_string)

    # Do the actual calculations:
    if top_solutions is True:
        top_mse = [1000000 for _ in range(100)]
        top_params = [[] for _ in range(100)]

    for combo in combos:
        if combo[2] % 1 == 0:
            print("Calculating for amp = {}, per = {}, shift_v = {}\tTime: {} seconds from the start."
                  .format(combo[0], combo[1], combo[2], round(time.time() - start, 2)))

        best_model_mse, phase_best_list = DesignCustomSineWave(family_list=family_list, how_many_gen=2,
                                              amp=combo[0], per=combo[1], shift_h=0, shift_v=combo[2])
        if top_solutions is True:
            if best_model_mse < top_mse[0]:
                for i in range(98, -1, -1):  # reversed order
                    top_mse[i + 1] = top_mse[i]
                    top_params[i + 1] = top_params[i]
                top_mse[0] = best_model_mse
                top_params[0] = [combo[0], combo[1], combo[2]]

        if write_file is True:
            mse_file.write(str(best_model_mse) + "\t")

    if top_solutions is True:
        print("\nTop 100 Solutions from {} combinations\n".format(len(combos)))
        for counter, (mse, params) in enumerate(zip(top_mse, top_params)):
            print("\tTop #{}: \tMean Squared Error = {}\tParameters = {}".format(counter + 1, mse, params))

    if write_file is True:
        mse_file.close()

    # Print the timing:
    time_total = time.time() - start
    time_total = time_total/86400, time_total/3600, time_total/60, time_total
    time_total = [round(time, 2) for time in time_total]
    print("\nDone... Horray! For {} combos it only took {} days or {} hours or {} minutes or {} seconds."
          .format(len(combos), time_total[0], time_total[1], time_total[2], time_total[3]))


# Call the function:
FindBestSineWaveFit(amp_st=2.0, amp_en=2.0, per_st=6.0, per_en=7.0, sft_st=12.0, sft_en=12.5,
                        increment=0.5, write_file=False, top_solutions=True)


