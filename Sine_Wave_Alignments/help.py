import numpy as np

amp = np.linspace(3.8, 4.0, 40 + 1)
per = np.linspace(11.0, 20.0, 90 + 1)
shi = np.linspace(17.0, 19.0, 20 + 1)

print (amp)
print (per)
print (shi)

print (len(amp) * len(per) * len(shi))