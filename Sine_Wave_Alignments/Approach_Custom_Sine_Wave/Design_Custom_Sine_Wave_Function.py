# TODO: Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
#       and align families to minimize loss across the entire dataset - plot the best fit!

import numpy as np
import matplotlib.pyplot as plt

# Define sine function:
def sine_function(x, amp, per, shift_h, shift_v):
    return amp * np.sin(2 * np.pi / per * x + shift_h) + shift_v

# Define true function:
def DesignCustomSineWave(file, amp, per, shift_h, shift_v):
    """ Create sine waves with unknown amp, per, shift_h and shift_v in combinatorial manner
        and align families to minimize loss across the entire dataset - plot the best fit!

    :param file:        //generation_3_families.txt  -> absolute directory (string)
    :param amp:
    :param per:
    :param shift_h:
    :param shift_v:
    :return:            None yet.
    """

    # Extract families' CCTs:
    family_list = []
    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Gen_1" and line[0] != "Cell_ID":
            family = [float(line[1]), float(line[4]), float(line[7])]
            if all(value > 12.00 and value < 24.00 for value in family):
                family_list.append(family)

    # Prepare the sine wave specified by the function parameters:
    repeats = 3
    x_sine = np.linspace(0, repeats * per + 1, int(repeats * per * 5))
    y_sine = sine_function(x=x_sine, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
    #plt.plot(x_sine, y_sine, color="dodgerblue")

    # Create the return variable - list of all best MSE that could be fitted for each family:
    mse_best_list = []

    for family in family_list:
        mse_list = []
        mse_family = 100
        phase_family = 0

        for phase in np.linspace(0, per + 1, int(per * 5)):

            # Create x & y axes:
            x_data = np.array([phase, phase + family[0], phase + family[0] + family[1]])
            y_data_true = np.array(family)
            y_data_sine = sine_function(x=x_data, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)

            # Calculate mean squared error:
            mse = (np.square(y_data_true - y_data_sine)).mean(axis=None)
            mse_list.append(mse)

            #print ("Mean Square Error = {}; for Phase {} for Family {} for Sine Wave: {} * sin(2*pi/{}*x + {}) + {}"
            #       .format(mse, phase, family, amp, per, shift_h, shift_v))


            # Update the lowest mse & the phase when such number was reached:
            if mse < mse_family:
                mse_family = mse
                phase_family = phase

        #print ("Lowest MSE reached: {} for Phase: {}".format(mse_family, phase_family))

        # Plot the best result for the family:
        x_best = np.array([phase_family, phase_family + family[0], phase_family + family[0] + family[1]])
        y_best = np.array(family)
        #plt.scatter(x=x_best, y=y_best)

        # Append the lowest MSE for this model:
        mse_best_list.append(mse_family)

    best_model_mse = round(np.sum(mse_best_list), 2)

    """
    plt.xticks(np.arange(0, repeats * per + 1, 6))
    plt.xlabel("Oscillation Period / Time [hours]")
    plt.ylabel("Cell Cycle Duration [hours]")
    plt.title("Sine Wave Parameters: y(x) = {} * sin(2*pi/{}*x + {}) + {}\nSum of Lowest MSE per each family = {}"
                .format(amp, per, shift_h, shift_v, best_model_mse))
    plt.grid(axis="both")
    plt.show()
    plt.close()
    """

    return best_model_mse

