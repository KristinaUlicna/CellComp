# TODO: Fit a sine wave onto a SINGLE 3-generational family lineage
# Tutorial here: https://astrofrog.github.io/py4sci/_static/15.%20Fitting%20models%20to%20data.html

import numpy as np
from scipy import optimize


def SineWaveFitting(file, print_stats=False):
    """ Fitting onto sine wave for 3-generational families.
        CURVE FIT CANNOT BE PERFORMED ON 2 DATAPOINTS! -> 2-generational family is not enough!
        Only includes CCTs greater than 12.00 and smaller than 24.00! TODO: Add outliers as well!

    Task:
        - calculate the parameters of a sine wave which fits perfectly onto each individual family
        - normalise this sine wave to have a positive amp and no shift_h - therefore oscillates from 0 upwards
        - calculate the phase of the points (=by how much you need to move them to the right on the x-axis) to restore maximum fit

    Sine wave:
        Equation:   amp * np.sin(2 * np.pi / per * x + shift_h) + shift_v
        Parameters:
                    static:     period      -> 24 hours
                                shift_h     -> 0 (after phasing the data on their x-axis)
                    dynamic:    amplitude   -> can be changed to absolute value; abs(amp)
                                shift_v     -> will always be positive (correspond to CCT range for each family)
    Args:
        file (str, directory)   -> absolute directory to file storing data in the following format:
                                        Gen_1	Gen_1	Gen_1	Gen_2	Gen_2	Gen_2	Gen_3	Gen_3	Gen_3
                                        Cell_ID	CCT	    Gener	Cell_ID	CCT	    Gener	Cell_ID	CCT	    Gener
        print_stats (bool)      -> visualuse stats if you wish.

    Return:
        cell_id_list (list)     -> stores cell_IDs of analysed family; [0] - grandparent, [1] - parent, [2] - child)
        y-data_list (list)      -> stores raw cell cycle durations [hours] of the cell_IDs above
        params_list (list)      -> stores amp, shift_h, shift_v of an ideally fitted sine wave per family
        phase_list (list)       -> (float) = phase which is to be added to each x-data point to preserve sine wave fit
    """

    cell_IDs_list = []
    y_data_list = []
    params_list = []
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
            phase = 0.0
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

            # Calculate the phase based on your fitted sine wave parameters:
            # Phase must correspond to shifts onto: abs(amp) * np.sin(2*np.pi/24 * x + 0) + shift_v
            phase = abs((shift_h * 24) / (2 * np.pi))

            if shift_h < 0:
                phase = 24 - phase
            if abs(shift_h) > 6.00 and abs(shift_h) < 12.00:
                phase = 24 - abs(phase)
            if abs(shift_h) > 12.00 and abs(shift_h) < 18.00:
                phase = phase + 48
            if amp < 0:
                phase = phase + 12

            if print_stats is True:
                print ("\nData on the y-axis: {}".format(y_data))
                print ("Data on the x-axis: {}".format(x_data))
                print ("\tParameters:\nAmplitude\t= {}\nPeriod\t\t= 2*pi*24\nShift H:\t= {}\nShift V:\t= {}"
                        .format(round(amp, 2), round(shift_h, 2), round(shift_v, 2)))
                print ("Calculated phase = {}\n\tfor 'y = abs(amp) * np.sin(2*np.pi/24 * x + 0) + shift_v'".format(phase))

            # Append the lists for return after loop is finished:
            cell_IDs_list.append([lineage[0][0], lineage[1][0], lineage[2][0]])
            y_data_list.append(y_data)
            params_list.append(params)
            phase_list.append(phase)

    return cell_IDs_list, y_data_list, params_list, phase_list
