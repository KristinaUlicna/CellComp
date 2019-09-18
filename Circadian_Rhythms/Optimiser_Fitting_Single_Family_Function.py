# TODO: Fit a sine wave onto a SINGLE 3-generational family lineage
# Tutorial here: https://astrofrog.github.io/py4sci/_static/15.%20Fitting%20models%20to%20data.html

import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

def FitSineWave_SingleFamily(file, show=False):
    """ Fitting onto sine wave for 3-generational families.

    Args:
        file (str)      -> absolute directory to file storing data in the following format:
                                Gen_1	Gen_1	Gen_1	Gen_2	Gen_2	Gen_2	Gen_3	Gen_3	Gen_3
                                Cell_ID	CCT	    Gener	Cell_ID	CCT	    Gener	Cell_ID	CCT	    Gener
        show (bool)     -> whether to visualise the graph:
                                False by default.
    Note:
        CURVE FIT CANNOT BE PERFORMED ON 2 DATAPOINTS!

    Sine wave parameters:
        Static:     period will always be static -> 24 hours
        Dynamic:    amp, shift_h, shift_v
            Can you fit with anchoring other parameters?
    """

    cell_IDs_list = []
    params_list = []
    y_data_phased_list = []
    x_data_phased_list = []
    phase_list = []

    for line in open(file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Gen_1" and line[0] != "Cell_ID":
            line = [float(value) if "." in value else int(value) for value in line]

            # Generate the data for Y-axis which are just the cell cycle durations:
            if len(line) <= 6:
                lineage = [line[0:3], line[3:6]]
                y_data = np.array([lineage[0][1], lineage[1][1]])
            else:
                lineage = [line[0:3], line[3:6], line[6:9]]
                y_data = np.array([lineage[0][1], lineage[1][1], lineage[2][1]])

            # Check if all CCTs are between 12-28 hours - exclude outliers:
            if any(cct < 12.0 for cct in y_data) or any(cct > 24.0 for cct in y_data):
                continue

            # X-axis starts at 'phase' (=unknown) & adds the Y-time points:
            phase = 0.0             # phase = horizontal shift of all my points (not the sine wave, defined as 'shift_h')
            x_data = [phase]
            for cct in y_data:
                phase += cct
                x_data.append(phase)
            x_estimate = x_data.pop(-1)
            x_data = np.array(x_data)

            # Now fit the sine wave onto your points:
            def sine_function(x, amp, shift_h, shift_v):
                return amp * np.sin(2 * np.pi / 24 * x + shift_h) + shift_v

            params, params_covariance = optimize.curve_fit(sine_function, x_data, y_data)
            amp, shift_h, shift_v = params[0], params[1], params[2]
            """
            print ("\nData on the y-axis: {}".format(y_data))
            print ("Data on the x-axis: {}".format(x_data))
            print ("\tParameters:\nAmplitude\t= {}\nPeriod\t\t= 2*pi*24\nShift H:\t= {}\nShift V:\t= {}"
                    .format(round(amp, 2), round(shift_h, 2), round(shift_v, 2)))
            """
            # Create data to illustrate the full sine wave:
            y_estimate = sine_function(x_estimate, *params)
            repeats = 3
            x_sine = np.arange(0, repeats * 24 + 1, 1)
            y_sine = sine_function(x_sine, *params)     # TIP: the star will call the whole list of params

            # Now plot the points:
            plt.plot(x_sine, y_sine, color="dodgerblue", alpha=0.8, label='Fitted Sine Wave')
            plt.scatter(x=x_data, y=y_data, color="forestgreen", label="Datapoints: {}".format(x_data))
            plt.scatter(x=x_estimate, y=y_estimate, color="plum", label="Estimate Raw")
            plt.axvline(x=24.0, color="gold", linestyle="dashed")
            plt.axvline(x=48.0, color="gold", linestyle="dashed")
            plt.xticks(np.arange(0, repeats * 24 + 1, 4))
            plt.xlabel("Oscillation period [hours]")
            plt.ylabel("Cell Cycle Duration [hours]")
            #plt.title("Sine wave equation: {} * sin(2*pi*/24 * x + {}) + {}"
            #          .format(round(amp, 2), round(shift_h, 2), round(shift_v, 2)))
            #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
            #plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Per_24/Sine_Wave_Cells_{}_{}_{}.png"
            #             .format(lineage[0][0], lineage[1][0], lineage[2][0]), bbox_inches="tight")
            #plt.show()
            #plt.close()


            #TODO: Calculate the phase?
            phase = abs((shift_h * 24) / (2 * np.pi))

            if shift_h < 0:
                phase = 24 - phase
            if abs(shift_h) > 6.00 and abs(shift_h) < 12.00:
                phase = 24 - abs(phase)
            if abs(shift_h) > 12.00 and abs(shift_h) < 18.00:
                phase = phase + 48
            if amp < 0:
                phase = phase + 12

            y_data_phased = y_data
            x_data_phased = [value + phase for value in x_data]
            x_data_phased = np.array(x_data_phased)

            x_sine_phased = x_sine
            y_sine_phased = sine_function(x=x_sine_phased, amp=abs(amp), shift_h=0, shift_v=shift_v)

            plt.plot(x_sine_phased, y_sine_phased, color="firebrick", label="Normed Sine Wave")
            plt.scatter(x=x_data_phased, y=y_data_phased, color="orange",
                        label="Datapoints: {}".format([round(item, 2) for item in x_data_phased]))
            plt.scatter(x=x_estimate+phase, y=y_estimate, color="deeppink", label="Estimate Phased")

            plt.axhline(y=shift_v, color="grey", linestyle="dashed")
            plt.title("OLD Sine wave equation: {} * sin(2*pi*/24 * x + {}) + {}\n"
                      "NEW Sine wave equation: {} * sin(2*pi*/24 * x) + {}\n"
                      "Data points PHASE = {}".format(round(amp, 2), round(shift_h, 2), round(shift_v, 2),
                                                      round(abs(amp), 2), round(shift_v, 2), round(phase, 2)))
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

            if show is True:
                plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Per_24_Pha_Custom/Sine_Wave_Cells_{}_{}_{}.png"
                            .format(lineage[0][0], lineage[1][0], lineage[2][0]), bbox_inches="tight")
                #plt.show()
                plt.close()

            cell_IDs_list.append([lineage[0][0], lineage[1][0], lineage[2][0]])
            params_list.append(params)
            y_data_phased_list.append(y_data_phased)
            x_data_phased_list.append(x_data_phased)
            phase_list.append(phase)

    return cell_IDs_list, params_list, y_data_phased_list, x_data_phased_list, phase_list
