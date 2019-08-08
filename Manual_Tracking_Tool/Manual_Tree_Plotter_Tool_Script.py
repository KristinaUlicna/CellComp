# TODO: Automate this if you can:
# Currently, the script plots manually-entered cell tracking data onto a scatter plot.
#       Note: This structure captures max. 4 full generations (fifth would have no room to be plotted).
# This is cell_ID #14 from '17_07_24' 'pos13' xml_file.

import matplotlib.pyplot as plt

x_0 = [0, 0]
y_0 = [0, 123]

x_1 = [-18, 18, -18, 18]
y_1 = [123, 123, 330, 361]

x_2 = [-26, -10, -26, -10, 10, 26, 10, 26]
y_2 = [330, 330, 545, 554, 361, 361, 624, 624]

x_3 = [-30, -22, -30, -22, -14, -6, -14, -6, 6, 14, 6, 14, 22, 30, 22, 30]
y_3 = [545, 545, 796, 856, 554, 554, 808, 785, 624, 624, 919, 861, 613, 613, 859, 880]

x_4 = [-32, -28, -24, -20, -16, -12, -8, -4, 4, 8, 12, 16, 20, 24, 28, 32]
y_4 = [1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104, 1104]

x_4 = x_4 * 2
y_4 = y_4 + [796, 796, 856, 856, 808, 808, 785, 785, 919, 919, 861, 861, 859, 859, 880, 880]

print (x_4)
print (len(x_4))
print (y_4)
print (len(y_4))

plt.scatter(x=x_0, y=y_0)
plt.scatter(x=x_1, y=y_1)
plt.scatter(x=x_2, y=y_2)
plt.scatter(x=x_3, y=y_3)
plt.scatter(x=x_4, y=y_4)
plt.xlim(-35, 35)
plt.ylim(-50, 1150)
plt.ylabel("Absolute time [frames]")
plt.title("Cell_ID #14 from '17_07_24' & 'pos13' - manually drown")
plt.show()
plt.close()
