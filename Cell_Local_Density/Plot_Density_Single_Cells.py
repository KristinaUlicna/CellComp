#TODO: Make plots of x=time & y=density for all cells in '17_07_31' and 'pos8' example file:

import matplotlib.pyplot as plt
import yaml
import time
start_time = time.process_time()


# Do the analysis for 1 example file:
example_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Density_Txt_Files/170731pos8density.txt"

dictionary = {}
for string in open(example_file, "r"):
    dictionary = yaml.load(string)
    print ("String -> Dictionary (len = {}): {} in {} minutes.".format(len(dictionary), type(dictionary), round((time.process_time() - start_time) / 60, 2)))


for key, value in dictionary.items():
    frame_list = []
    density_list = []
    if len(value) > 180:
        for frame in value:
            frame_list.append(int(frame[0]))
            density_list.append(float(frame[1]))

        plt.scatter(x=frame_list, y=density_list)
        plt.title("Cell-ID #{} density plot".format(key))
        plt.xlabel("Frame #")
        plt.ylabel("Density [μm-2]")
        plt.ylim(0, 0.001)

        #plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/ExampleDensityCellID4511.jpeg")
        plt.show()
        plt.close()

print ("It took {} mins.".format((time.process_time() - start_time) / 60))