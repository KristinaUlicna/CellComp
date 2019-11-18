# TODO: Access the information in the segmented.hdf5 file: especially the positions of the cell centres at every frame

import h5py
import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt


def GetXandYcoordinatesPerFrame(hdf5_file, frame=0):
    """

    :param hdf5_file:
    :return: x_gfp, y_gfp
    """

    f = h5py.File(hdf5_file, 'r')
    x_gfp, y_gfp, x_rfp, y_rfp = [], [], [], []

    for object in list(f["frames"]["frame_{}".format(frame)]["coords"]):
        if int(object[4]) == 1:
            x_gfp.append(object[1])
            y_gfp.append(object[2])
        elif int(object[4]) == 2:
            x_rfp.append(object[1])
            y_rfp.append(object[2])
        else:
            raise TypeError("Cell type is unknown; not GFP = 1, not RFP = 2.")

    return x_gfp, y_gfp, x_rfp, y_rfp


def ConvertXandYcoordinates(x_gfp, y_gfp, x_rfp, y_rfp, print_lists=False):
    """ Convert the x & y coordinates so you can plot the centroids on 2D plane.
        Principle = x being y and y being 1200-x.
        Return these arrays.
    """

    x_gfp_to_plot = y_gfp
    y_gfp_to_plot = [1200 - item for item in x_gfp]
    x_rfp_to_plot = y_rfp
    y_rfp_to_plot = [1200 - item for item in x_rfp]

    if print_lists is True:
        print("X_GFP: {}".format(x_gfp_to_plot))
        print(min(x_gfp_to_plot), max(x_gfp_to_plot))
        print("Y_GFP: {}".format(y_gfp_to_plot))
        print(min(y_gfp_to_plot), max(y_gfp_to_plot))
        print("X_RFP: {}".format(x_rfp_to_plot))
        print(min(x_rfp_to_plot), max(x_rfp_to_plot))
        print("Y_RFP: {}".format(y_rfp_to_plot))
        print(min(y_rfp_to_plot), max(y_rfp_to_plot))

    return x_gfp_to_plot, y_gfp_to_plot, x_rfp_to_plot, y_rfp_to_plot


def PlotXandYcoordinatesPerFrame(hdf5_file, frame=0):
    """ Plot the centroids on 2D plane. Watch out for the x being y and y being 1200-x. """

    x_gfp, y_gfp, x_rfp, y_rfp = GetXandYcoordinatesPerFrame(hdf5_file=hdf5_file, frame=frame)
    x_gfp, y_gfp, x_rfp, y_rfp = ConvertXandYcoordinates(x_gfp, y_gfp, x_rfp, y_rfp)

    # Plot to visualise:
    plt.scatter(x=x_gfp, y=y_gfp, color="green")
    plt.scatter(x=x_rfp, y=y_rfp, color="magenta")
    plt.title("Cells in Frame #{} according to 'segmented.hdf5'".format(frame))
    plt.xlabel("X coordinate [pixels]")
    plt.ylabel("Y coordinate [pixels]")
    plt.xlim(0, 1600)
    plt.ylim(0, 1200)
    plt.show()
    plt.close()


def DrawVoronoiTesselation(hdf5_file, frame=0):
    """

    wanted structure: np.array([[3, 0], [4.2, 1], [0, 8], [1, 5], [1, 1], [1, 2], [3.5, 0], [4, 1], [6, 6]])


    :return:
    """
    x_gfp, y_gfp, x_rfp, y_rfp = GetXandYcoordinatesPerFrame(hdf5_file=hdf5_file, frame=frame)
    x_gfp, y_gfp, x_rfp, y_rfp = ConvertXandYcoordinates(x_gfp, y_gfp, x_rfp, y_rfp)

    # Restructure so that you get a matrix; merge channels as the cell identity is not important in this case:
    points = []
    for x, y in zip(x_gfp + x_rfp, y_gfp + y_rfp):
        points.append([x, y])
    points = np.array(points)

    vor = sp.Voronoi(points)
    print(vor)
    tri = sp.Delaunay(points)
    print(tri)

    fig = sp.voronoi_plot_2d(vor)
    fig = sp.delaunay_plot_2d(tri)
    plt.show()
    plt.close()


# Call the function to test:
filename = '/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/HDF/segmented.hdf5'
PlotXandYcoordinatesPerFrame(hdf5_file=filename, frame=0)
DrawVoronoiTesselation(hdf5_file=filename, frame=0)