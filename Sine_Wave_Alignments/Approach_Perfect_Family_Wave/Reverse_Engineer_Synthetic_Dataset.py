# TODO: Create a synthetic dataset - how would the data need to look like if we were able to fit the sine wave on them?

# You want to reverse engineer data which would fit onto your 'ideal' curve:
# Eq: y = amp * np.sin (2* np.pi / 24 * x + shift_h) + shift_v
# Without shift_h:  2.63 * np.sin (2 * np.pi / 24 * x) + 17.18

import numpy as np
import matplotlib.pyplot as plt

def sine_function(x, amp, per, shift_h, shift_v):
    return amp * np.sin(2*np.pi/per * x + shift_h) + shift_v

amp, per, shift_h, shift_v = 2.63, 24.0, 0, 17.18

repeats = 4
x_sine = np.linspace(0, repeats * 24 + 1, 100)
y_sine = sine_function(x_sine, amp, per, shift_h, shift_v)


# Now do the reverse engineering for 5-generational families with phases ranging between 0-24:
def SynthesizeData(phase):
    """ Phase ranges from 0 to 24 with increments of 0.2. """

    x_list = [phase]
    y_list = []

    while len(x_list) < 5 or len(y_list) < 5:
        x = x_list[-1]
        y = sine_function(x=x, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
        x_list.append(y+x)
        y_list.append(y)
    x_list = x_list[:-1]

    return x_list, y_list


phase_range = np.linspace(0, 24, 120)
print (phase_range)

x_data_0 = []
y_data_0 = []
for phase in list(phase_range.tolist()):
    x_list, y_list = SynthesizeData(phase=phase)
    plt.scatter(x=x_list, y=y_list, color="purple", alpha=0.2, zorder=2) # label="Fake Data Point",
    y_data_0.append(y_list)
    x_data_0.append([value - x_list[0] for value in x_list])


# Now plot the thing:
plt.plot(x_sine, y_sine, color="turquoise", label="Ideal Sine Wave", zorder=1)
plt.axhline(y=shift_v, color="grey", linestyle="dashed", zorder=0)
plt.axvline(x=24.0, color="gold", linestyle="dashed", zorder=0)
plt.axvline(x=48.0, color="gold", linestyle="dashed", zorder=0)
plt.axvline(x=72.0, color="gold", linestyle="dashed", zorder=0)
plt.xticks(np.arange(0, repeats * 24 + 1, 4))
plt.xlabel("Oscillation Period [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Ideal Sine Wave")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Summary_All_Cells/Ideal_Wave.png", bbox_inches="tight")
plt.show()
plt.close()


# Now plot the non-phased data:
for x, y in zip(x_data_0, y_data_0):
    plt.scatter(x=x, y=y)

plt.xlabel("Oscillation Period [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Relationships between generations in an ideal family\n"
          "Equation: {} * np.sin (2 * np.pi / {} * x + {}) + {}"
          .format(amp, per, shift_h, shift_v))
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Sine_Wave/Summary_All_Cells/Ideal_Wave_Relationships.png",
            bbox_inches="tight")
plt.show()
plt.close()