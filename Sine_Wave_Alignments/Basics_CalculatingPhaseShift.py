import matplotlib.pyplot as plt
import numpy as np

def sinus(x, amp, shift_h, shift_v):
    return amp * np.sin(2*np.pi/24 * x + shift_h) + shift_v

def cosinus(x, amp, shift_h, shift_v):
    return amp * np.cos(2*np.pi/24 * x + shift_h) + shift_v


x = np.arange(0, 4801, 1)
x = [element/100 for element in x]
x = np.array(x)

"""
amp, shift_h, shift_v = 1.53, 1.68, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="dodgerblue", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))
"""

amp, shift_h, shift_v = -1.53, 1.68, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="forestgreen", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))

y_point = [14.33, 17.0, 16.53]
x_point = [0, 14.33, 31.33]

plt.scatter(x=x_point, y=y_point, color="forestgreen")

"""
amp, shift_h, shift_v = -1.53, 1, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="firebrick", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))
"""
amp, shift_h, shift_v = -1.53, 0, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="orange", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))

y_point = [14.33, 17.0, 16.53]
x_point = [6.42, 20.75, 37.75]

plt.scatter(x=x_point, y=y_point, color="orange")


print (x)
print (y)

"""
amp, shift_h, shift_v = 1.53, 13.68, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="plum", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))


amp, shift_h, shift_v = 1.53, 1.68, 15.85
y = cosinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="orange", label="{} * cos(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))

amp, shift_h, shift_v = -1.53, 1.68, 15.85
y = cosinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="firebrick", label="{} * cos(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))
"""
plt.title("Sine Wave shifts")
plt.xlabel("Time [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.xticks(np.arange(0, 49, 4))
plt.axhline(y=15.85, color="grey", linestyle="dashed")
plt.axvline(x=24.00, color="gold", linestyle="dashed")
plt.axvline(x=12.00, color="gold", linestyle="dashed", alpha=0.5)
plt.axvline(x=36.00, color="gold", linestyle="dashed", alpha=0.5)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)
plt.show()
plt.close()