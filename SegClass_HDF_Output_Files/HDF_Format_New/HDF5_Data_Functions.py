# TASK: Function to access data stored in the new structure of the HDF file after the September update.
#
# The structure is:           ['objects', 'tracks']
#       'objects'       ->    ['obj_type_1', 'obj_type_2']        (if both channels)
#       'obj_type_1'    ->    ['coords', 'labels', 'map'] where:
#           'coords' = [t (frame), x, y, z, type (1=GFP, 2=RFP)]
#           'labels' = [_, _, _, _, _, _] -> probability of an object is in inter-, prometa-, meta-, anaphase or apoptosis
#           'map' = [0, X] for frame #0 -> cumulative cell count (or rather 'segmented object count') per each frame.
#                   last number of previous frame is starting number of following frame, [0, 95], [95, 193], [193, 286],...
#                   To get cell count per frame, subtract value[1] from value [0] from the specified frame.


import h5py
import numpy as np
import pandas as pd
import scipy.spatial as sp
import matplotlib.pyplot as plt


def GetCellCountPerFrame(hdf5_file, frame=0):

    f = h5py.File(hdf5_file, 'r')
    objects = list(f["objects"])
    cell_count = 0
    for channel in [1, 2]:
        if 'obj_type_{}'.format(channel) in objects:
            frame_cells = list(f["objects"]["obj_type_{}".format(channel)]["map"])[frame]
            cell_count += frame_cells[1] - frame_cells[0]

    return cell_count



def GetXandYcoordsPerFrame(hdf5_file, frame=0):
    """ Iterates through the whole hdf5_file and returns
        4 nested lists of the length of 1 (single frame)
        with all 'x' & 'y' GFP and RFP cells coordinates.

    :param hdf5_file:
    :param frame:
    :return:
    """

    x_coords, y_coords = [[] for _ in range(2)], [[] for _ in range(2)],

    f = h5py.File(hdf5_file, 'r')
    objects = list(f["objects"])
    print (objects)

    for channel in objects:
        index = list(f["objects"][channel]["map"])[frame]
        selection = list(f["objects"][channel]["coords"])[index[0]:index[1]]
        for centroid in selection:
            x_coords[int(channel.split("obj_type_")[-1])-1].append(centroid[0])
            y_coords[int(channel.split("obj_type_")[-1])-1].append(centroid[1])

    x_gfp_coords = x_coords[0]
    y_gfp_coords = y_coords[0]
    x_rfp_coords = x_coords[1]
    y_rfp_coords = y_coords[1]

    return x_gfp_coords, y_gfp_coords, x_rfp_coords, y_rfp_coords



def GetXandYcoordsPerFrameSLOW(hdf5_file, frame=0):
    """ Iterates through the whole hdf5_file and returns
        4 nested lists of the length of 1 (single frame)
        with all 'x' & 'y' GFP and RFP cells coordinates.

    :param hdf5_file:
    :param frame:
    :return:
    """

    f = h5py.File(hdf5_file, 'r')
    channel_num = len(list(f['objects']))
    x_gfp_coords, y_gfp_coords, x_rfp_coords, y_rfp_coords = [], [], [], []

    for obj_type in range(channel_num):
        for centroid in list(f["objects"]["obj_type_{}".format(obj_type + 1)]["coords"]):
            if int(centroid[0]) == frame:
                if int(centroid[4]) == 1:
                    x_gfp_coords.append(centroid[1])
                    y_gfp_coords.append(centroid[2])
                if int(centroid[4]) == 2:
                    x_rfp_coords.append(centroid[1])
                    y_rfp_coords.append(centroid[2])

    return x_gfp_coords, y_gfp_coords, x_rfp_coords, y_rfp_coords


def GetXandYcoordsPerMovie(hdf5_file):
    """ Iterates through the whole hdf5_file and returns
        4 nested lists of the length of the movie
        with all x & y GFP and RFP cells coordinates.

    :param hdf5_file:
    :return:
    """

    f = h5py.File(hdf5_file, 'r')
    channel_num = len(list(f['objects']))
    cell_type = list(f['objects'])[0]
    movie_length = len(list(f["objects"][str(cell_type)]["map"]))
    x_gfp_coords, y_gfp_coords, x_rfp_coords, y_rfp_coords = [[[] for _ in range(movie_length)] for _ in range(4)]

    for obj_type in range(channel_num):
        for centroid in list(f["objects"]["obj_type_{}".format(obj_type+1)]["coords"]):
            if int(centroid[4]) == 1:
                x_gfp_coords[int(centroid[0])].append(centroid[1])
                y_gfp_coords[int(centroid[0])].append(centroid[2])
            if int(centroid[4]) == 2:
                x_rfp_coords[int(centroid[0])].append(centroid[1])
                y_rfp_coords[int(centroid[0])].append(centroid[2])

    return x_gfp_coords, y_gfp_coords, x_rfp_coords, y_rfp_coords


def CreateDataFramePerMovie(hdf5_file):
    """ Create Data Frame for 3D plotting."""

    """
    x_gfp_coords, y_gfp_coords, x_rfp_coords, y_rfp_coords = GetXandYcoordsPerMovie(hdf5_file=hdf5_file)

    movie_length = None

    if not x_gfp_coords:
        movie_length = len(x_gfp_coords)
    else:
        movie_length = len(x_rfp_coords)
    print (movie_length)

    frames = list(range(movie_length))
    df = pd.DataFrame(data=None, index=, columns=['x', 'y', 'frame', 'cell_type'])
    """

    hdf = pd.HDFStore(path=hdf5_file, mode='r')
    print (hdf.keys())
    df1 = hdf.get(key='objects')
    print (df1)

    #df = pd.read_hdf(path_or_buf=hdf5_file)
    #print (df)



f1 = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos0/HDF/segmented.hdf5"
f2 = "/Volumes/lowegrp/Data/Kristina/MDCK_Sc_Tet-_Pure/17_01_19/pos6/HDF/segmented.hdf5"
f3 = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/HDF/segmented.hdf5"


"""
frame = 500

for filename in [f3]:
    #i = GetCellCountPerFrame(hdf5_file=filename, frame=frame)
    i, j, k, l = GetXandYcoordsPerFrame(hdf5_file=filename, frame=frame)
    m, n, o, p = GetXandYcoordsPerFrameSLOW(hdf5_file=filename, frame=frame)

    print (len(i+k))
    print (len(m+o))
"""