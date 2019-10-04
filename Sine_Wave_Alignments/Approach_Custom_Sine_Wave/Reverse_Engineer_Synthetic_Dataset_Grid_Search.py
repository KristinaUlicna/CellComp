# TODO: Create a synthetic dataset - how would the data need to look like if we were able to fit the sine wave on them?

# You want to reverse engineer data which would fit onto your 'ideal' curve:
# Eq: y = amp * np.sin (2* np.pi / per * x + shift_h) + shift_v
# Without shift_h:  2.63 * np.sin (2 * np.pi / per * x) + 17.18

import numpy as np
import matplotlib.pyplot as plt

def sine_function(x, amp, per, shift_h, shift_v):
    return amp * np.sin(2*np.pi/per * x + shift_h) + shift_v

amp, per, shift_h, shift_v = 4.59, 11.75, 0, 17.71

repeats = int(72 / per)
x_sine = np.linspace(0, repeats * per, int(per*10))
y_sine = sine_function(x_sine, amp, per, shift_h, shift_v)


# Now do the reverse engineering for 5-generational families with phases ranging between 0-24:
def SynthesizeData(phase, total_gen):
    """ Phase ranges from 0 to 24 with increments of 0.2. """

    x_list = [phase]
    y_list = []

    while len(x_list) < total_gen or len(y_list) < total_gen:
        x = x_list[-1]
        y = sine_function(x=x, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
        x_list.append(y+x)
        y_list.append(y)
    x_list = x_list[:-1]

    return x_list, y_list


phase_range = np.linspace(0, per, int(per*10) + 1)
print (phase_range)


x_data_0 = []
y_data_0 = []
for phase in list(phase_range.tolist()):
    x_list, y_list = SynthesizeData(phase=phase, total_gen=3)
    plt.scatter(x=x_list, y=y_list, color="purple", alpha=0.2, zorder=2) # label="Fake Data Point",
    y_data_0.append(y_list)
    x_data_0.append([value - x_list[0] for value in x_list])


# Now plot the thing:
plt.plot(x_sine, y_sine, color="turquoise", label="Ideal Sine Wave", zorder=1)
plt.axhline(y=shift_v, color="grey", linestyle="dashed", zorder=0)
for i in range(1, repeats):
    plt.axvline(x=per*i, color="gold", linestyle="dashed", zorder=0)
plt.xticks(np.linspace(0, repeats * per, repeats * 2 + 1), rotation=45)
plt.xlabel("Oscillation Period [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Ideal Sine Wave: y(x) = {} * sin(2 * pi / {} * x) + {}".format(amp, per, shift_v))
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Ideal_Wave_3_gen_round_2.png", bbox_inches="tight")
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
plt.grid(which="both")
plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Ideal_Wave_Relationships_3_gen_round_2.png", bbox_inches="tight")
plt.show()
plt.close()