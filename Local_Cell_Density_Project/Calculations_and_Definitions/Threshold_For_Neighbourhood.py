# Calculate how many pixels apart must 2 cells be to be considered neighbours according to Alan's python code:

import json
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

def GetXandYcoordinates(cell_id):
    """ Get the coordinates by reading a json file.

    Args:
        Cell_id (float) -> which cell_id's coordinates you want.

    Return:
        List of x, y coordinates of a given cell.
    """

    directory = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/tracks/"
    # You know that cell id='23' is close to cell id='24' and 'id='35' (both GFP, forget RFP for now)

    tracks_json_file = directory + "tracks_GFP/track_{}_GFP.json".format(cell_id)

    x_list = []
    y_list = []

    with open(tracks_json_file) as json_file:
        data = json.load(json_file)
        for x, y in zip(data['x'], data['y']):
            x_list.append(x)
            y_list.append(y)
    return x_list, y_list


x_23, y_23 = GetXandYcoordinates(cell_id=23)
x_24, y_24 = GetXandYcoordinates(cell_id=24)
x_35, y_35 = GetXandYcoordinates(cell_id=35)


def CalculateNhoodDistance(x_list_target, y_list_target, x_list_query, y_list_query):
    """ Numerical value below which two cells are considered to be neighbours.
        Determine this by calculating the distance between them using the Pythagorean Theorem.
    """
    dist_list = []

    for x_t, y_t, x_q, y_q in zip(x_list_target, y_list_target, x_list_query, y_list_query):
        dist = np.sqrt((x_t-x_q)**2+(y_t-y_q)**2)
        dist_list.append(dist)

    return dist_list


# Call the function:
dist_list_24 = CalculateNhoodDistance(x_23, y_23, x_24, y_24)
print (len(dist_list_24), dist_list_24)

dist_list_35 = CalculateNhoodDistance(x_23, y_23, x_35, y_35)
print (len(dist_list_35), dist_list_35)

for counter, item in enumerate(dist_list_35):
    print (counter, item)

for counter, item in enumerate(dist_list_24):
    print (counter, item)

# You can now clearly see that the threshold for counting something in is equal to 100.00 pixels!