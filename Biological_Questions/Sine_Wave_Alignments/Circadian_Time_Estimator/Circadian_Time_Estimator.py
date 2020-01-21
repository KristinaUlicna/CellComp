# Try to estimate cell cycle duration of next generation by just fitting the previous generations on the sine wave:
#       2nd generation by fitting Gen#1 on the wave (= perfect fit)
#       3rd generation by fitting Gen#1 & Gen#2 on the wave (= imperfect but still pretty good fit)

import numpy as np
import matplotlib.pyplot as plt
# TODO: Import the old-fashioned function! Now you have a duplicate!
from Biological_Questions.Sine_Wave_Alignments.Approach_Grid_Search.Design_Custom_Sine_Wave_Function \
    import DesignCustomSineWave, PrepareFamilyList, sine_function


def EstimateNextGenerationCCT(estimate_of, estimate_from, source_file,
                              amp=4.5, per=19.0, shift_h=0, shift_v=18.5):
    """ Estimate the cell cycle duration of generations for which you know the real CCT values.
        Compare the expected data to observed data. Plot the results.

    :param estimate_of:     (list of int)   -> Which generation you want to estimate (should be +1 compared to est_from)
    :param estimate_from:   (list of int)   -> Which generation(s) you want to use to fit on the curve & use to est_of
    :param source_file:     (int)           -> Which file to source the data from. Can only be 2 or 3 generational.
    :param amp:             (float)
    :param per:             (float)
    :param shift_h:         (float) -> 0 by default. Don't change. Shift_h is calculated in a different way.
    :param shift_v:         (float)
    :return:
    """

    # Raise a few exception to ensure you won't run into a problem later:
    if source_file != 2 and source_file != 3:
        raise ValueError("Incorrect file specified. Please choose between 2- or 3-generational file.")

    #if how_many_gen > estimate_of[-1]:
    #    raise ValueError("Cannot estimate higher generation than the number of generations initially produced:\n"
    #                     "You don't have the observed CCT value to compare your expected CCT value to.")

    # Process the source file & extract the family CCT data you want to process further:
    file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/generation_{}_families.txt".format(source_file)
    family_list = PrepareFamilyList(file=file, how_many_gen=estimate_of[0])
    families = len(family_list)

    print (family_list)
    print (len(family_list))

    # Import the function to fit your point onto the pre-defined wave:
    # TODO: Import from original, raw function - change to have the option to return the phase_best_list!
    _, phase_list = DesignCustomSineWave(family_list=family_list, how_many_gen=len(estimate_from), show=False,
                                              amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)

    phase_list = np.array([round(value, 2) for value in phase_list])
    print(phase_list)
    print(len(phase_list))


    # Break the multilayered list of CCTs (=y_data) into individual lists by generation:
    y_data = [[] for _ in range(estimate_of[0])]

    for element in family_list:
        for index, value in enumerate(element):
            y_data[index].append(value)

    for index, gen_list in enumerate(y_data):
        y_data[index] = np.array(gen_list)

    print (y_data)
    print (y_data[0])
    print (type(y_data[0]))
    print (type(y_data[0][0]))


    # Create a corresponding multilayered list of x_axis values, using the correct phasing:
    x_data = [phase_list for _ in range(estimate_of[0])]

    for i in range(1, len(x_data)):
        x_data[i] = np.add(x_data[i-1], y_data[i-1])

    print (y_data)
    print (len(y_data))
    print (len(y_data[0]))
    print (x_data)
    print (len(x_data))
    print(len(x_data[0]))

    # Create the estimates for the last available generation & compare it to what is known:
    estimate = sine_function(x=x_data[-1], amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
    print (estimate)
    print (len(estimate))

    diff_total = np.subtract(y_data[-1], estimate)
    diff_absol = np.absolute(diff_total)

    repeats = source_file + len(estimate_from)
    x_sine = np.linspace(0, per * repeats, int(per * repeats * 10 + 1))
    y_sine = sine_function(x=x_sine, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)

    # Plot the sine wave:
    plt.plot(x_sine, y_sine, color="dodgerblue", label="Sine Wave", zorder=0)

    plt.scatter(x=x_data[estimate_from[-1]-1], y=y_data[estimate_from[-1]-1],
                s=10, color="orange", label="Aligned Gen #{}".format(estimate_from))
    if len(estimate_from) > 1:
        plt.scatter(x=x_data[estimate_from[-2] - 1], y=y_data[estimate_from[-2] - 1],
                    s=10, color="gold", label="Aligned Gen #{}".format(estimate_from))

    plt.scatter(x=x_data[estimate_of[0]-1], y=y_data[estimate_of[0]-1],
                s=10, color="forestgreen", label="Observed Gen #{}".format(estimate_of))
    plt.scatter(x=x_data[estimate_of[0]-1], y=estimate,
                s=10, color="firebrick", label="Expected Gen #{}".format(estimate_of))

    plt.xticks(np.arange(0, repeats * per + 1, 6))
    plt.xlabel("Oscillation Period / Time [hours]")
    plt.ylabel("Cell Cycle Duration [hours]")
    plt.title("Sine Wave Parameters: y(x) = {} * sin(2 * pi / {} * x) + {}".format(amp, per, shift_v))
    plt.grid(axis="both")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/estimates/"
                "Estimate_CCT_Gen{}_from{}_File{}_Amp{}_Per{}_Sft{}_SineWave.png"
                .format(estimate_of[-1], estimate_from[-1], source_file, amp, per, shift_v), bbox_inches="tight")
    plt.show()
    plt.close()

    # Plot the differences:
    plt.scatter(x=list(range(len(diff_total))), y=diff_total, color="forestgreen", label="Observed\nCCT data")
    plt.scatter(x=list(range(len(diff_total))), y=[0 for _ in range(len(diff_total))], color="firebrick", label="Calculated\nestimate\n(normalised)")
    plt.xlabel("Family Count")
    plt.ylabel("Cell Cycle Duration [hours]")
    plt.title("Sine Wave Parameters: y(x) = {} * sin(2 * pi / {} * x) + {}".format(amp, per, shift_v))
    plt.grid(axis="y")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/estimates/"
                "Estimate_CCT_Gen{}_from{}_File{}_Amp{}_Per{}_Sft{}_DiffTotal.png"
                .format(estimate_of[-1], estimate_from[-1], source_file, amp, per, shift_v), bbox_inches="tight")
    plt.show()
    plt.close()

    plt.scatter(x=list(range(len(diff_absol))), y=diff_absol, color="plum", label="Difference (absolute)\nExpected - Observed")
    plt.xlabel("Family Count")
    plt.ylabel("Cell Cycle Duration [hours]")
    plt.title("Sine Wave Parameters: y(x) = {} * sin(2 * pi / {} * x) + {}".format(amp, per, shift_v))
    plt.grid(axis="y")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/estimates/"
                "Estimate_CCT_Gen{}_from{}_File{}_Amp{}_Per{}_Sft{}_DiffAbsol.png"
                .format(estimate_of[-1], estimate_from[-1], source_file, amp, per, shift_v), bbox_inches="tight")
    plt.show()
    plt.close()


EstimateNextGenerationCCT(estimate_of=[2], estimate_from=[1], source_file=2, amp=4.5, per=19.0, shift_h=0, shift_v=18.5)
EstimateNextGenerationCCT(estimate_of=[2], estimate_from=[1], source_file=3, amp=4.5, per=19.0, shift_h=0, shift_v=18.5)
EstimateNextGenerationCCT(estimate_of=[3], estimate_from=[1, 2], source_file=3, amp=4.5, per=19.0, shift_h=0, shift_v=18.5)
EstimateNextGenerationCCT(estimate_of=[2], estimate_from=[1], source_file=3, amp=4.55, per=11.75, shift_h=0, shift_v=17.70)
EstimateNextGenerationCCT(estimate_of=[3], estimate_from=[1, 2], source_file=3, amp=4.55, per=11.75, shift_h=0, shift_v=17.70)
