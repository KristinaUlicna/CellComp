# TODO:

import numpy as np
from matplotlib import pyplot as plt
from Sine_Wave_Alignments.Optimiser_Fitting_Function import SineWaveFitting


def PlotSuperSineWave(amp_shiftH_shiftV=False, amp_shiftV=False, amp_only=False):
    """
    """

    file = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"
    cell_IDs_list, y_data_list, params_list, phase_list = SineWaveFitting(file=file, print_stats=False)

    for cell_IDs, y_data, params, phase in zip(cell_IDs_list, y_data_list, params_list, phase_list):

        # Create raw data points:
        shft = 0.0
        x_axis_raw = [shft]
        for cct in y_data:
            shft += cct
            x_axis_raw.append(shft)
        x_axis_raw = np.array(x_axis_raw[:-1])

        # Create raw sine data:
        def sine_function(x, amp, shift_h, shift_v):
            return amp * np.sin(2*np.pi/24 * x + shift_h) + shift_v

        amp, shift_h, shift_v = params[0], params[1], params[2]

        repeats = 3
        x_line = np.linspace(0, repeats * 24 + 1, 200)
        y_sine = sine_function(x=x_line, amp=amp, shift_h=shift_h, shift_v=shift_v)

        # Create phased data points:
        x_axis_normed = [phase + value for value in x_axis_raw]

        if amp_shiftH_shiftV is True:
            #y_sine_normed = sine_function(x_line, amp=amp, shift_h=shift_h, shift_v=0)
            plt.plot(x_line, y_sine, color="dodgerblue")
            plt.scatter(x=x_axis_raw, y=y_data, color="forestgreen")

        if amp_shiftV is True:
            y_sine_normed = sine_function(x_line, amp=abs(amp), shift_h=0, shift_v=shift_v)
            plt.plot(x_line, y_sine_normed, color="firebrick")
            plt.scatter(x=x_axis_normed, y=y_data, color="orange")

        if amp_only is True:
            y_sine_normed = sine_function(x_line, amp=abs(amp), shift_h=0, shift_v=0)
            plt.plot(x_line, y_sine_normed, color="firebrick")
            plt.scatter(x=x_axis_normed, y=y_data, color="orange")

        plt.title("All Amps & Shifts_h & Shifts_v")
        plt.axvline(x=24.0, color="gold", linestyle="dashed", zorder=0)
        plt.axvline(x=48.0, color="gold", linestyle="dashed", zorder=0)
        plt.xticks(np.arange(0, repeats * 24 + 1, 4))
        plt.xlabel("Oscillation Period [hours]")
        plt.ylabel("Cell Cycle Duration [hours]")
    plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Summary_All_Cells/Sine_Wave_All_Cells_Amp.png", bbox_inches="tight")
    plt.show()
    plt.close()


PlotSuperSineWave(amp_shiftH_shiftV=True, amp_shiftV=False, amp_only=False)
PlotSuperSineWave(amp_shiftH_shiftV=False, amp_shiftV=True, amp_only=False)
PlotSuperSineWave(amp_shiftH_shiftV=False, amp_shiftV=False, amp_only=True)