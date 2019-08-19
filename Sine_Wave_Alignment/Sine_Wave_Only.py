import numpy as np
import matplotlib.pyplot as plt

fs = 80                             # sample rate
f = 2                               # the frequency of the signal

x = np.arange(0, fs+1, 1)           # the points on the x axis for plotting
y = np.sin(2*np.pi*f * (x/fs))      # compute the value (amplitude) of the sin wave at the for each sample

plt.plot(x, y, "r-")
plt.grid(which="both")
plt.xlabel("Time [hours]")
plt.ylabel("Amplitude")
plt.show()
plt.close()
