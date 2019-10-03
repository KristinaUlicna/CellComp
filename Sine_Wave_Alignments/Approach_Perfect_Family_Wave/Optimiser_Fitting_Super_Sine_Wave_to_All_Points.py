# TODO: Fit a new sine wave on all points:

from Circadian_Rhythms.Optimiser_Fitting_Single_Family_Function import FitSineWave_SingleFamily
from scipy.optimize import curve_fit
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt

file = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"
cell_IDs_list, params_list, y_data_phased_list, x_data_phased_list, phase_list = FitSineWave_SingleFamily(file=file, show=True)

x_data = []
y_data = []
for x, y in zip(x_data_phased_list, y_data_phased_list):
    x = x.tolist()
    y = y.tolist()
    plt.scatter(x=x, y=y, color="purple")
    x_data.append(x)
    y_data.append(y)

x_data = list(chain.from_iterable(x_data))
y_data = list(chain.from_iterable(y_data))

repeats = 3
x_sine = np.arange(0, repeats * 24 + 1, 1)

# TODO: With shift_h:
def sine_function_with(x, amp, shift_h, shift_v):
    return amp * np.sin(2 * np.pi / 24 * x + shift_h) + shift_v

params, params_covariance = curve_fit(sine_function_with, x_data, y_data)
print (params)
print (params_covariance)
y_sine = sine_function_with(x_sine, amp=params[0], shift_h=params[1], shift_v=params[2])
plt.plot(x_sine, y_sine, color="dodgerblue", label="With shift_h: {} * sin(2*pi/24 * x + {}) + {}"
         .format(round(params[0], 2), round(params[1], 2), round(params[2], 2)))
plt.axhline(y=params[2], color="dodgerblue", alpha=0.8, linestyle="dashed")

# TODO: WithOUT shift_h:
def sine_function_without(x, amp, shift_v):
    return amp * np.sin(2 * np.pi / 24 * x) + shift_v

params, params_covariance = curve_fit(sine_function_without, x_data, y_data)
print (params)
print (params_covariance)
y_sine = sine_function_without(x_sine, amp=params[0], shift_v=params[1])
plt.plot(x_sine, y_sine, color="forestgreen", label="WithOUT shift_h: {} * sin(2*pi/24 * x) + {}"
         .format(round(params[0], 2), round(params[1], 2)))
plt.axhline(y=params[1], color="forestgreen", alpha=0.8, linestyle="dashed")


# Decorate & visualise
plt.axvline(x=24.0, color="gold", linestyle="dashed")
plt.axvline(x=48.0, color="gold", linestyle="dashed")
plt.ylim(12, 24)
plt.xticks(np.arange(0, repeats * 24 + 1, 4))
plt.xlabel("Oscillation Period [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Sine Waves Fitted to All points with ideal fit")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Sine_Wave_Fitted_All_Points.png", bbox_inches="tight")
plt.show()
plt.close()

