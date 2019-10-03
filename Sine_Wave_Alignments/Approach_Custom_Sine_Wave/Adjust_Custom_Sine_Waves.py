from Circadian_Rhythms.Optimiser_Fitting_Single_Family_Function import FitSineWave_SingleFamily
import numpy as np
import matplotlib.pyplot as plt

file = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"
y_data_list, params_list = FitSineWave_SingleFamily(file=file, individual=False, show=False)

for counter, (y_data, params) in enumerate(zip(y_data_list, params_list)):
    #print(counter, y_data, params)
    if counter != 3:
        continue

    print(counter, y_data, params)

    amp, shift_h, shift_v = params[0], params[1], params[2]
    phase = 0.0         # phase = horizontal shift of all my points (not the sine wave, defined as 'shift_h')
    x_data = [phase]
    for cct in y_data:
        phase += cct
        x_data.append(phase)
    x_estimate = x_data.pop(-1)
    x_data = np.array(x_data)

    def sine_function(x, amp, shift_h, shift_v):
        return amp * np.sin(2 * np.pi / 24 * x + shift_h) + shift_v

    repeats = 3
    x_sine = np.arange(0, repeats * 24 + 1, 1)
    y_sine = sine_function(x_sine, amp=amp, shift_h=shift_h, shift_v=shift_v)

    plt.plot(x_sine, y_sine, color="dodgerblue", label="Sine Wave RAW")
    plt.scatter(x=x_data, y=y_data, color="forestgreen", label="Data; phase = 0.0")

    #TODO: Now try to do the shifts:
    phase = (shift_h * 24) / (2 * np.pi)
    print("ORIGINAL PHASE = {}".format(phase))

    if amp > 0 and shift_h > 0:
        phase = (shift_h * 24) / (2 * np.pi)
        print ("PHASE = {}".format(phase))

    if amp > 0 and shift_h < 0:
        phase = 24 - abs(phase)
        #phase = 24 - abs((shift_h * 24) / (2 * np.pi)) + 24
        print("PHASE = {}".format(phase))

    if amp < 0 and shift_h > 0:
        phase = ((shift_h * 24) / (2 * np.pi)) + 12
        print("PHASE = {}".format(phase))

    if amp < 0 and shift_h < 0:
        phase = 24 - (abs((shift_h * 24) / (2 * np.pi)) - 24) + 12
        #phase = 24 - (abs((shift_h * 24) / (2 * np.pi)) - 24)
        print("PHASE = {}".format(phase))

    # Re-name new parameters:
    #amp = abs(amp)
    #shift_h = 0


    y_data_phased = y_data
    x_data_phased = [value + phase for value in x_data]

    x_sine_phased = x_sine
    y_sine_phased = sine_function(x=x_sine_phased, amp=abs(amp), shift_h=0, shift_v=shift_v)

    plt.plot(x_sine_phased, y_sine_phased, color="firebrick", label="Sine Wave NORMED")
    plt.scatter(x=x_data_phased, y=y_data_phased, color="orange", label="Data; phase = {}".format(round(phase, 2)))
    plt.title("Sine Wave equation: {} * sin(2*pi/24*x + {}) + {}".format(amp, shift_h, shift_v))
    plt.axvline(x=24.0, color="gold", linestyle="dashed")
    plt.axvline(x=48.0, color="gold", linestyle="dashed")
    plt.axhline(y=shift_v, color="grey", linestyle="dashed")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Per_24_Pha_Custom/Sine_Wave_Cell_{}.png"
                .format(counter), bbox_inches="tight")
    plt.show()
    plt.close()
