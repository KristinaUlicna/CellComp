#TODO: Design a sine wave and fit the data onto it by minimizing loss:
#TODO: Automatise for all points:
#TODO: Estimate for the last data point!
#TODO: Instead of just doing min & max, plot your ccts into means±sems to see how well they are distributed!

import numpy as np
import matplotlib.pyplot as plt


# Design an arbitrary sine wave now - you restricted your CCTs range 12 - 24 hours. Use this information
def sin_function(x, amp, per, shift_h, shift_v):
    return amp * np.sin(2 * np.pi / per * x + shift_h) + shift_v

amp, per, shift_h, shift_v = 6, 24, 0, 18
sin_repeats = 3
x_sin = np.arange(0, 24 * sin_repeats + 1)
y_sin = sin_function(x=x_sin, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)

# Now plot the thing:
plt.plot(x_sin, y_sin, label="Sine Wave")
plt.xlabel("Oscillation period [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Fitting data onto the sine wave\ny = {} * sin(2*pi / {} * x + {}) + {}".format(amp, per, shift_h, shift_v))
plt.xticks(np.arange(0, 24 * sin_repeats + 1, 4))
plt.yticks(np.arange(shift_v - amp, shift_v + amp + 1, 2))
plt.grid(b=None, axis="y", which="both")

plt.axvspan(0, 12, alpha=0.7, color='moccasin')
plt.axvspan(12, 24, alpha=0.7, color='peachpuff')
if sin_repeats > 1:
    plt.axvspan(24, 36, alpha=0.7, color='moccasin')
    plt.axvspan(36, 48, alpha=0.7, color='peachpuff')
if sin_repeats > 2:
    plt.axvspan(48, 60, alpha=0.7, color='moccasin')
    plt.axvspan(60, 72, alpha=0.7, color='peachpuff')
#plt.legend()
#plt.show()
#plt.close()


# Play with an example dataset:
"""
lineage = ['1675', '13.8', '1', '3215', '15.0', '2', '5522', '20.07', '3']

x_shift = 0         # TODO: UNKNOWN
y_data = [float(lineage[1]), float(lineage[4]), float(lineage[4])]
x_data = [x_shift, x_shift + y_data[0], x_shift + y_data[0] + y_data[1]]


# Plot these onto the graph:
plt.scatter(x=x_data, y=y_data, color="forestgreen", label="Real Data", zorder=5)


# For those x-data, calculate what their y-values (on the sin) are:
y_sine = []
for value in x_data:
    y_sine.append(sin_function(x=value, amp=amp, per=per, pha=pha, y_shift=y_shift))

print ("X-DATA: True =\t{}".format(x_data))
print ("Y-DATA: True =\t{}".format(y_data))
print ("Y-DATA: Sine =\t{}".format(y_sine))

# Calculate how different these values are:
y_diff = [round(abs(item_1 - item_2), 2) for item_1, item_2 in zip(y_data, y_sine)]
print (y_diff)
y_diff = sum(y_diff)
print (y_diff)

# Visualise the figure:
plt.legend()
plt.show()
plt.close()
"""

# TODO: Automate for this single dataset:
def MinimizeDataLoss(file):
    gens_total = file.split("_families.txt")[0][-1]

    for line in open(file, "r"):
        line = line.rstrip().split("\t")

        # Exclude headers:
        if line[0] == 'Gen_1' or line[0] == 'Cell_ID':
            continue

        if len(line) <= 6:
            y_data = [float(line[1]), float(line[4])]
        else:
            y_data = [float(line[1]), float(line[4]), float(line[7])]

        # Condition to only include families which take MORE THAN 10.00 hours & LESS THAN 24.00 hours to divide:
        if any(value < 12.00 or value > 24.00 for value in y_data):
            continue

        lowest_y_difference = 100       # ridiculously high!
        best_x_shift = 0
        low_diff_list = []
        best_x_shift_list = []

        for x_shift in range(0, 24 + 1, 1):
            if len(line) <= 6:
                x_data = [x_shift, x_shift + y_data[0]]
            else:
                x_data = [x_shift, x_shift + y_data[0], x_shift + y_data[0] + y_data[1]]

            # For those x-data, calculate what their y-values (on the sin) are:
            y_sine = []
            for value in x_data:
                y = sin_function(x=value, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
                y_sine.append(round(y, 2))

            #print("X-DATA: True =\t{}".format(x_data))
            #print("Y-DATA: True =\t{}".format(y_data))
            #print("Y-DATA: Sine =\t{}".format(y_sine))

            # Calculate how different these values are:
            y_diff = [round(abs(item_1 - item_2), 2) for item_1, item_2 in zip(y_data, y_sine)]
            y_diff = round(sum(y_diff), 2)

            # Update your UNKNOWN parameter if lower than in previous iteration:
            if y_diff < lowest_y_difference:
                lowest_y_difference = y_diff
                best_x_shift = x_shift

        print ("Lowest difference: {}".format(lowest_y_difference))
        print ("Best X-shift: {}".format(best_x_shift))

        # You found the best shift, so now store those:
        low_diff_list.append(lowest_y_difference)
        best_x_shift_list.append(best_x_shift)

        # Plot it!
        if len(line) <= 6:
            x_data_new = [best_x_shift, best_x_shift + y_data[0]]
        else:
            x_data_new = [best_x_shift, best_x_shift + y_data[0], best_x_shift + y_data[0] + y_data[1]]

        plt.scatter(x=x_data_new, y=y_data, zorder=5)

    plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Optimised_Gen_{}_families_Sine_Wave.jpeg".format(gens_total),
                bbox_to_inches="tight")
    plt.show()
    plt.close()


#file = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"
#MinimizeDataLoss(file=file)

#file = "/Users/kristinaulicna/Documents/Rotation_2/generation_2_families.txt"
#MinimizeDataLoss(file=file)