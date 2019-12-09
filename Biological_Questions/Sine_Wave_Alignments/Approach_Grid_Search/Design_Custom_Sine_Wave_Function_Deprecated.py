# "Grid Search" Approach:
#       Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
#       and align families to minimize loss across the entire dataset - plot the best fit!

import numpy as np
import matplotlib.pyplot as plt


def PrepareFamilyList(file, how_many_gen):
    """ Prepare list which the following function will read to optimize the parameters.

    Args:
        :arg file:
        :arg how_many_gen

    Return:
        :param family_list:     (list of floats) CCT of gen#1, CCT of gen#2, CCT of gen#3 cell in the family
    """

    family_list = []
    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Gen_1" and line[0] != "Cell_ID":
            family = []
            if how_many_gen == 2:
                family = [float(line[1]), float(line[4])]
            if how_many_gen == 3:
                family = [float(line[1]), float(line[4]), float(line[7])]
            if all(value > 12.00 and value < 24.00 for value in family):
                family_list.append(family)
    return family_list


def sine_function(x, amp, per, shift_h, shift_v):
    """ Function to calculate y from x with 4 dynamic sine wave parameters. """
    return amp * np.sin(2 * np.pi / per * x + shift_h) + shift_v


# Define the GRID SEARCH function:
def DesignCustomSineWave(family_list, how_many_gen, amp, per, shift_h, shift_v,
                         show=False, print_phase_mse=False, return_phases=False):

    """ "Grid Search" Approach:
            Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
            and align families to minimize loss across the entire dataset - plot the best fit!

    :param family_list:         (list)  ->
    :param how_many_gen:        (int)   ->
    :param amp:                 (float) ->
    :param per:                 (float) ->
    :param shift_h:             (float) ->
    :param shift_v:             (float) ->
    :param show:                (bool)  ->
    :param print_phase_mse:     (bool)  ->

    :return:                    best_model_mse (float) -> the best possible phasing of families
                                                        to reach lowest mse for given model
    """

    # Specify how many generations do your families have:
    if int(how_many_gen) != 3 and int(how_many_gen) != 2:
        raise Exception("Warning, number of generations to consider is not specified: how_many_gen must be 2 or 3!")

    # Prepare the sine wave specified by the function parameters:
    repeats = int(72.0 / per)
    if repeats <= 1:
        repeats += 1

    x_sine = np.linspace(0, repeats * per + 1, int(repeats * per * 5))
    y_sine = sine_function(x=x_sine, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
    if show is True:
        plt.plot(x_sine, y_sine, color="dodgerblue")

    # Create the return variable - list of all best MSE that could be fitted for each family which will be summed:
    mse_best_list = []
    phase_best_list = []

    for family in family_list:
        mse_list = []
        mse_family = 100
        phase_family = 0

        # Increments of 0.1 for chosen period:
        for phase in np.linspace(0, per, int(per*10) + 1):

            # Create x & y axes:
            x_data = np.array([phase, phase + family[0]])
            if how_many_gen == 3:
                x_data = np.array([phase, phase + family[0], phase + family[0] + family[1]])
            y_data_true = np.array(family)
            y_data_sine = sine_function(x=x_data, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)

            # Calculate mean squared error:
            mse = (np.square(y_data_true - y_data_sine)).mean(axis=None)
            mse_list.append(mse)

            if print_phase_mse is True:
                print ("Mean Square Error = {}; for Phase {} for Family {} for Sine Wave: {} * sin(2*pi/{}*x + {}) + {}"
                       .format(mse, phase, family, amp, per, shift_h, shift_v))


            # Update the lowest mse & the phase when such number was reached:
            if mse < mse_family:
                mse_family = mse
                phase_family = phase

        if print_phase_mse is True:
            print ("Lowest MSE reached: {} for Phase: {}".format(mse_family, phase_family))

        # Plot the best result for the family:
        x_best = np.array([phase_family, phase_family + family[0]])
        if how_many_gen == 3:
            x_best = np.array([phase_family, phase_family + family[0], phase_family + family[0] + family[1]])
        y_best = np.array(family)
        if show is True:
            plt.scatter(x=x_best, y=y_best)

        # Append the lowest MSE for this model:
        mse_best_list.append(mse_family)
        phase_best_list.append(phase_family)

    sum = float(np.sum(mse_best_list))
    best_model_mse = round(sum, 2)

    # Annotate the plot:
    if show is True:
        plt.xticks(np.arange(0, repeats * per + 1, 6))
        plt.xlabel("Oscillation Period / Time [hours]")
        plt.ylabel("Cell Cycle Duration [hours]")
        plt.title("Sine Wave Parameters: y(x) = {} * sin(2*pi/{}*x + {}) + {}\n"
                  "Sum of Lowest MSE per each family = {}"
                  .format(amp, per, shift_h, shift_v, best_model_mse))
        plt.grid(axis="both")
        plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Top_Solution_Sine_Wave_{}_gen_families.png"
                    .format(how_many_gen), bbox_inches="tight")
        plt.show()
        plt.close()

    return best_model_mse
