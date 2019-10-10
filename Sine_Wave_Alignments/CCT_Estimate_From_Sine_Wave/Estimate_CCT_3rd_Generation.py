#TODO: Now that you know the ideal sine wave for 3-generational families,
#   try to calculate by how much off the 3rd generation is:

import numpy as np
import matplotlib.pyplot as plt
from Sine_Wave_Alignments.Data_Shape_Summary import CharacteriseDataShape
from Sine_Wave_Alignments.Approach_Custom_Sine_Wave.Design_Custom_Sine_Wave_Function \
    import sine_function, PrepareFamilyList


amp, per, shift_h, shift_v = 4.65, 19.25, 0, 18.65
file = "/Users/kristinaulicna/Documents/Rotation_2/generation_3_families.txt"

# Prepare the sine wave specified by the function parameters:
repeats = int(72.0 / per)
if repeats <= 1:
    repeats += 1

x_sine = np.linspace(0, repeats * per + 1, int(repeats * per * 5))
y_sine = sine_function(x=x_sine, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
plt.plot(x_sine, y_sine, color="dodgerblue", label="Sine Wave")

# Create the return variable - list of all best MSE that could be fitted for each family which will be summed:
mse_best_list = []
phase_best_list = []

cct_gens = CharacteriseDataShape(file=file, limit_low=12, limit_high=24)
gen_1_true = cct_gens[0]
gen_2_true = cct_gens[1]
gen_3_true = cct_gens[2]

print (gen_1_true)
print (gen_2_true)
print (gen_3_true)

gen_3_exp_list = []

for gen_1, gen_2, gen_3 in zip(gen_1_true, gen_2_true, gen_3_true):
    family = [gen_1, gen_2]

    mse_list = []
    mse_family = 100
    phase_family = 0

    # Increments of 0.1 for chosen period:
    for phase in np.linspace(0, per, int(per*10) + 1):

        # Create x & y axes:
        x_data = np.array([phase, phase + family[0]])
        y_data_true = np.array(family)
        y_data_sine = sine_function(x=x_data, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)

        # Calculate mean squared error:
        mse = (np.square(y_data_true - y_data_sine)).mean(axis=None)
        mse_list.append(mse)

        # Update the lowest mse & the phase when such number was reached:
        if mse < mse_family:
            mse_family = mse
            phase_family = phase

    print ("Lowest MSE reached: {} for Phase: {}".format(mse_family, phase_family))

    # Now compare the 3rd gen datapoint between expected & observed:
    gen_3_x = np.array([phase_family + gen_1 + gen_2])
    gen_3_obs = gen_3
    gen_3_exp = sine_function(x=gen_3_x, amp=amp, per=per, shift_h=shift_h, shift_v=shift_v)
    gen_3_exp_list.append(gen_3_exp)

    # Plot the best result for the family:
    plt.scatter(x=gen_3_x, y=gen_3_obs, color="forestgreen")
    plt.scatter(x=gen_3_x, y=gen_3_exp, color="firebrick")

    # Append the lowest MSE for this model:
    mse_best_list.append(mse_family)
    phase_best_list.append(phase_family)

sum = float(np.sum(mse_best_list))
best_model_mse = round(sum, 2)

# Annotate the plot:
plt.scatter(x=0, y=shift_v, color="forestgreen", label="Observed")
plt.scatter(x=0, y=shift_v, color="firebrick", label="Expected")
plt.xticks(np.arange(0, repeats * per + 1, 6))
plt.xlabel("Oscillation Period / Time [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Sine Wave Parameters: y(x) = {} * sin(2*pi/{}*x + {}) + {}\nSum of Lowest MSE per each family = {}"
                .format(amp, per, shift_h, shift_v, best_model_mse))
plt.axhline(y=shift_v, linestyle="dashed", color="grey")
plt.xlim(32, 50)
plt.legend()
plt.show()
plt.close()


print ("MSE Best List: {}".format(mse_best_list))
print (len(mse_best_list))
print ("Phase Best List: {}".format(phase_best_list))
print (len(phase_best_list))
print ("Best Model MSE: {}".format(best_model_mse))


plt.scatter(x=list(range(0, 21)), y=gen_3_exp_list, color="firebrick", label="Expected")
plt.scatter(x=list(range(0, 21)), y=gen_3_true, color="forestgreen", label="Observed")
plt.title("ZOOM IN TO GENERATION #3\nSine Wave Parameters: y(x) = {} * sin(2*pi/{}*x + {}) + {}".format(amp, per, shift_h, shift_v))
plt.legend()
plt.show()
plt.close()

difference = [item_1 - item_2 for item_1, item_2 in zip(gen_3_exp_list, gen_3_true)]
difference_abs = [abs(item) for item in difference]
print (difference)
print (np.mean(difference))
print (np.std(difference))
print (np.median(difference))

plt.scatter(x=list(range(0, 21)), y=[0 for _ in range(0, 21)], color="firebrick", label="Expected")
plt.scatter(x=list(range(0, 21)), y=difference, color="forestgreen", label="Observed")
plt.title("RELATIVE DIFFERENCE\nSine Wave Parameters: y(x) = {} * sin(2*pi/{}*x + {}) + {}".format(amp, per, shift_h, shift_v))
plt.legend()
plt.show()
plt.close()

plt.scatter(x=list(range(0, 21)), y=[0 for _ in range(0, 21)], color="firebrick", label="Expected")
plt.scatter(x=list(range(0, 21)), y=difference_abs, color="forestgreen", label="Observed")
plt.title("ABSOLUTE DIFFERENCE\nSine Wave Parameters: y(x) = {} * sin(2*pi/{}*x + {}) + {}".format(amp, per, shift_h, shift_v))
plt.legend()
plt.show()
plt.close()
