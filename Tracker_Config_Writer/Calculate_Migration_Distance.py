import os
import json
import numpy as np
import matplotlib.pyplot as plt

def CalculateCellMigration(config_number=50):
    """ Uses Pythagorean Theorem to calculate the distance migrated by a cell between 2 tracks:
            c^2 = a^2 + b^2
        from which:
            c = sqrt(a^2 + b^2)
        from which:
            c = sqrt((x_1 - x_2)^2 + (x_1 - x_2)^2)
        where c (hypotenuse) is the distance migrated by the cell (in pixels) and
        a, b (legs, sides) are the differences between x1 and x2 or y1 and y2 coordinates, respectively.
    """

    dictionary = {}
    dr = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
           "tracks_try_50/tracks/tracks_RFP/".format(config_number)

    for track in range(1, len(os.listdir(dr)) + 1):
        file = dr + "track_{}_RFP.json".format(track)
        if os.path.exists(file):
            print("Processing 'track_{}_RFP.json'".format(track), end="\t")

            with open(file) as json_file:
                data = json.load(json_file)
                dist_list = []
                index = 0
                while index + 1 < len(data['t']):
                    x_1, y_1 = float(data['x'][index]), float(data['y'][index])
                    x_2, y_2 = float(data['x'][index+1]), float(data['y'][index+1])
                    dist = np.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
                    dist = round(dist, 2)
                    dist_list.append(dist)
                    index += 1
            if track not in dictionary:
                dictionary[track] = dist_list
        else:
            print("File 'track_{}_RFP.json' doesn't exist.".format(track), end="\t")
    print ("\n")

    return dictionary


dictionary = CalculateCellMigration()
print (dictionary)

for key, value in dictionary.items():
    #print ("{}: {}".format(key, value))
    try:
        values = np.mean(value), np.std(value), np.median(value), min(value), max(value)
        values = [round(item, 2) for item in values]
        print ("{}: mean = {}\tstd = {}\tmed = {}\tmin = {}\tmax = {}"
               .format(key, values[0], values[1], values[2], values[3], values[4]))
    except:
        continue


dr = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
     "tracks_try_50/migration_outliers/"
if not os.path.isdir(dr):
    os.makedirs(dr)
labels, data = [*zip(*dictionary.items())]  # 'transpose' items to parallel key, value lists
label_list = []
for label, datus in zip(labels, data):
    if len(datus) > 1:
        if max(datus) > 75:
            plt.boxplot(datus)
            plt.xlabel(label)
            plt.ylim(-10, 160)
            plt.ylabel("Distance migrated by the cell_ID [pixels]")
            plt.title("Outlier Cell_IDs which migrated way too far to be a single tracklet")
            plt.savefig(dr + "Outlier_{}_Boxplot.png".format(label), bbox_inches='tight')
            plt.show()
            plt.close()
