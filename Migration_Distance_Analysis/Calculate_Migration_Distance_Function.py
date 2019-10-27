import os
import json
import numpy as np
import matplotlib.pyplot as plt

def CalculateCellMigration(cell_ID, pos, date):
    """ Uses Pythagorean Theorem to calculate the distance migrated by a cell between 2 tracks:
            c^2 = a^2 + b^2
        from which:
            c = sqrt(a^2 + b^2)
        from which:
            c = sqrt((x_1 - x_2)^2 + (x_1 - x_2)^2)
        where c (hypotenuse) is the distance migrated by the cell (in pixels) and
        a, b (legs, sides) are the differences between x1 and x2 or y1 and y2 coordinates, respectively.

        Returns the mean, std and median distance migrated by the cell. Normalised for the cell cycle lifetime.
    """

    dictionary = {}
    file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/{}/{}/tracks/tracks_GFP/track_{}_GFP.json"\
                .format(date, pos, cell_ID)

    if not os.path.exists(file):
        print("File 'track_{}_RFP.json' doesn't exist\nDirectory: '{}'".format(cell_ID, file))

    with open(file) as json_file:
        data = json.load(json_file)
        dist_list = []
        index = 0
        while index + 1 < len(data['t']):
            x_1, y_1 = float(data['x'][index]), float(data['y'][index])
            x_2, y_2 = float(data['x'][index+1]), float(data['y'][index+1])
            dist = np.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
            dist_list.append(round(dist, 4))
            index += 1
        if cell_ID not in dictionary:
            dictionary[cell_ID] = dist_list
    return dictionary


def ExtractMigrationDistances():
    # Read the file to get the list of cells which you need the migration distance to be calculated for:
    merged_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"

    cell_ID_list = []
    dist_list = []

    for line in open(merged_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Cell_ID-posX-date":
            # Only include the cells which are in generation #1!
            if int(line[5]) == 1:
                try:
                    cell = line[0].split("-")
                    cell_ID, pos, date = int(cell[0]), cell[1], cell[2]
                    dictionary = CalculateCellMigration(cell_ID=cell_ID, pos=pos, date=date)
                    migration = list(dictionary.values())
                    cell_ID_list.append(cell_ID)
                    dist_list.append(migration)
                except:
                    continue

    return cell_ID_list, dist_list