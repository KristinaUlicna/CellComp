import matplotlib.pyplot as plt
import numpy as np

def sinus(x, amp, shift_h, shift_v):
    return amp * np.sin(2*np.pi/24 * x + shift_h) + shift_v

x = np.arange(0, 49, 1)

amp, shift_h, shift_v = 1.53, 1.68, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="dodgerblue", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))

amp, shift_h, shift_v = -1.53, 1.68, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="forestgreen", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))

amp, shift_h, shift_v = 1.53, 0, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="orange", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))

amp, shift_h, shift_v = -1.53, 0, 15.85
y = sinus(x=x, amp=amp, shift_h=shift_h, shift_v=shift_v)
plt.plot(x, y, color="firebrick", label="{} * sin(2*pi/24 * x + {}) + {}".format(amp, shift_h, shift_v))

plt.title("Sine Wave shifts")
plt.xlabel("Time [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.axhline(y=15.85, color="grey", linestyle="dashed")
plt.axvline(x=24.00, color="gold", linestyle="dashed")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)
plt.show()
plt.close()