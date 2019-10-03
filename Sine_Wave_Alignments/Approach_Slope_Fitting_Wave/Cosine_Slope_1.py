#TODO: Align the families onto cosine wave and plot the linear regression with the slope of 1:

import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt

def cosine_function(x, amp, per, shift_h, shift_v):
    return amp * np.cos(2*np.pi/per * x + shift_h) + shift_v

# Define the cosine wave:
amp, per, shift_h, shift_v = 6, 24, 0, 18
repeats = 2
x_wave = np.linspace(0, repeats * per + 1, 48 * repeats)
y_wave = cosine_function(x_wave, amp, per, shift_h, shift_v)

# Do linear regression for the linear part:
x_data = np.array([4, 6, 8])
y_data = cosine_function(x_data, amp, per, shift_h, shift_v)
regression = sp.linregress(x=x_data, y=y_data)
print (regression)      # meaning: y(x) = slope * x + intercept
slope, intercept = regression[0], regression[1]
y_regress = np.array([value * slope + intercept for value in x_data])

# Plot the thing:
st, en = 0, 12
plt.plot([st, en], [slope * st + intercept, slope * en + intercept], color="pink", zorder=1)
plt.scatter(x=x_wave, y=y_wave)
plt.ylim(11, 25)
plt.xticks(np.arange(0, repeats * per + 1, 6))
plt.xlabel("Oscillation period [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Linear Regression over Cosine Wave")
plt.show()
plt.close()
