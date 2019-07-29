# Plot an example cell density over time:
# TODO: Read the dictionary from file rather than from this script!

import matplotlib.pyplot as plt
import yaml
import time
start_time = time.process_time()

import sys
sys.path.append("../")
from Processing_MatLab_Files.Finding_Density_Values import FindDensitySpan


# Do the analysis for 1 example file:
file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos0/density/cellID_density.txt"
dictionary = {}
for string in open(file, "r"):
    dictionary = yaml.load(string)
    print ("String -> Dictionary (len = {}): {} in {} minutes.".format(len(dictionary), type(dictionary), round((time.process_time() - start_time) / 60, 2)))

# Example cellID = 4511:
frame_list = []
density_list = []
for key, value in dictionary.items():
    if key == 4511:
        for frame in value:
            frame_list.append(int(frame[0]))
            density_list.append(float(frame[1]))

print ("Frames:", len(frame_list), frame_list)
print ("Density:", len(density_list), density_list)
print ("Equal len?", len(frame_list) == len(density_list))


# Plot it's density:
"""
plt.scatter(x=frame_list, y=density_list)
plt.title("CellID #4511 density plot (generation #2)")
plt.xlabel("Frame #")
plt.ylabel("Density [units?]")
plt.ylim(0, 0.001)
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/ExampleDensityCellID4511.jpeg")
plt.show()
plt.close()
"""

# Find key density values:
density_values = []
for span in ["birth", "one_quarter", "half_way", "three_quarters", "mitosis"]:
    density_value = FindDensitySpan(density_list=density_list, span=span)
    density_values.append(density_value)
print ("Density values for cellID 4511: {}".format(density_values))