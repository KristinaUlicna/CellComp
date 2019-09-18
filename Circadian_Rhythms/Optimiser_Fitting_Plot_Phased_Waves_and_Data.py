# TODO: Produce the graphs:

from Circadian_Rhythms.Optimiser_Fitting_Single_Family_Function import FitSineWave_SingleFamily
import numpy as np
import matplotlib.pyplot as plt

file = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"
cell_IDs_list, params_list, y_data_phased_list, x_data_phased_list, phase_list = FitSineWave_SingleFamily(file=file, show=True)


for cell_IDs, params, y_data, x_data, phase in zip(cell_IDs_list, params_list, y_data_phased_list, x_data_phased_list, phase_list):
    def sin_func(x, amp, shift_h, shift_v):
        return amp * np.sin(2 * np.pi / 24 * x + shift_h) + shift_v

    repeats = 3
    x_sine = np.arange(0, repeats * 24 + 1, 1)
    y_sine = sin_func(x=x_sine, amp=abs(params[0]), shift_h=0, shift_v=params[2])
    plt.plot(x_sine, y_sine, color="firebrick", label="Normed Sine Wave")
    plt.scatter(x=x_data, y=y_data, color="orange", label="Phased Datapoints")
    plt.axhline(y=params[2], color="grey", linestyle="dashed")
    plt.axvline(x=24.0, color="gold", linestyle="dashed")
    plt.axvline(x=48.0, color="gold", linestyle="dashed")
    plt.xticks(np.arange(0, repeats * 24 + 1, 4))
    plt.xlabel("Oscillation Period [hours]")
    plt.ylabel("Cell Cycle Duration [hours]")
    plt.title("Phased Sine Wave Eq: {} * sin(2*pi/24 * x) + {}".format(round(abs(params[0]), 2), round(abs(params[2]), 2)))
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Per_24_Shift_h_0/Sine_Wave_Cells_{}_{}_{}.png"
                            .format(cell_IDs[0], cell_IDs[1], cell_IDs[2]), bbox_inches="tight")
    plt.show()
    plt.close()