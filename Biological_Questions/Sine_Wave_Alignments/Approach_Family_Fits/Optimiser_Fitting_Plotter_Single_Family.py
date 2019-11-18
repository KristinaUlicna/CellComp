# TODO:

import numpy as np
from matplotlib import pyplot as plt
from Biological_Questions.Sine_Wave_Alignments.Approach_Family_Fits import SineWaveFitting


def PlotFittedSineWave(raw_only=False, phased_only=False, both_raw_phased=False):
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

        # Create normed sine wave:
        y_sine_normed = sine_function(x_line, amp=abs(amp), shift_h=0, shift_v=shift_v)

        if raw_only is True:
            plt.plot(x_line, y_sine, color="dodgerblue", label="Sine Wave Raw")
            plt.scatter(x=x_axis_raw, y=y_data, color="forestgreen", label="Data points Raw")
            plt.axhline(y=shift_v, color="grey", linestyle="dashed", zorder=0)
            plt.axvline(x=24.0, color="gold", linestyle="dashed", zorder=0)
            plt.axvline(x=48.0, color="gold", linestyle="dashed", zorder=0)
            plt.xticks(np.arange(0, repeats * 24 + 1, 4))
            plt.xlabel("Oscillation Period [hours]")
            plt.ylabel("Cell Cycle Duration [hours]")
            plt.title("Sine Wave Equation: {} * sin(2*pi/24 * x + shift_h) + shift_v"
                  .format(round(amp, 2), round(shift_h, 2), round(shift_v, 2)))
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
            plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Raw_only/Sine_Wave_Cell_IDs_{}_{}_{}.png"
                        .format(cell_IDs[0], cell_IDs[1], cell_IDs[2]), bbox_inches="tight")
            #plt.show()
            plt.close()

        if phased_only is True:
            plt.plot(x_line, y_sine_normed, color="firebrick", label="Sine Wave Normed")
            plt.scatter(x=x_axis_normed, y=y_data, color="orange", label="Data points Phased")
            plt.axhline(y=shift_v, color="grey", linestyle="dashed", zorder=0)
            plt.axvline(x=24.0, color="gold", linestyle="dashed", zorder=0)
            plt.axvline(x=48.0, color="gold", linestyle="dashed", zorder=0)
            plt.xticks(np.arange(0, repeats * 24 + 1, 4))
            plt.xlabel("Oscillation Period [hours]")
            plt.ylabel("Cell Cycle Duration [hours]")
            plt.title("Sine Wave Eq: {} * sin(2*pi/24 * x) + shift_v\nPhase = {}"
                       .format(round(abs(amp), 2), round(shift_v, 2), round(phase, 2)))
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
            plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Phased_only/Sine_Wave_Cell_IDs_{}_{}_{}.png"
                        .format(cell_IDs[0], cell_IDs[1], cell_IDs[2]), bbox_inches="tight")
            #plt.show()
            plt.close()

        if both_raw_phased is True:
            plt.plot(x_line, y_sine, color="dodgerblue", label="Sine Wave Raw")
            plt.scatter(x=x_axis_raw, y=y_data, color="forestgreen", label="Data points Raw")
            plt.plot(x_line, y_sine_normed, color="firebrick", label="Sine Wave Normed")
            plt.scatter(x=x_axis_normed, y=y_data, color="orange", label="Data points Phased")
            plt.axhline(y=shift_v, color="grey", linestyle="dashed", zorder=0)
            plt.axvline(x=24.0, color="gold", linestyle="dashed", zorder=0)
            plt.axvline(x=48.0, color="gold", linestyle="dashed", zorder=0)
            plt.xticks(np.arange(0, repeats * 24 + 1, 4))
            plt.xlabel("Oscillation Period [hours]")
            plt.ylabel("Cell Cycle Duration [hours]")
            plt.title("OLD Sine Wave Eq: {} * sin(2*pi/24 * x + shift_h) + shift_v\n"
                      "NEW Sine Wave Eq: {} * sin(2*pi/24 * x) + shift_v\n"
                      "Phase = {}".format(round(amp, 2), round(shift_h, 2), round(shift_v, 2),
                                    round(abs(amp), 2), round(shift_v, 2), round(phase, 2)))
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
            plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Both_Raw_Phased/Sine_Wave_Cell_IDs_{}_{}_{}.png"
                        .format(cell_IDs[0], cell_IDs[1], cell_IDs[2]), bbox_inches="tight")
            #plt.show()
            plt.close()


PlotFittedSineWave(raw_only=False, phased_only=False, both_raw_phased=False)
