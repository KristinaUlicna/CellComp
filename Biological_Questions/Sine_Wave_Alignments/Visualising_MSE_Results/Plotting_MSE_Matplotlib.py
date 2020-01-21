# TODO: Read the partially written file with MSE scores and try to plot it in 3D with matplotlib & plotly

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

mse_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE_Grid_Search.txt"

def PlotSurfaceMSE(amplitude):
    # Pair up the parameters with your actual results from the file: First, process only for amps 2.0, 2.1, 2.2
    params = []
    """
    amplitude = 2.0
    elev = [45, 35], [75, 60]
    """
    for amp in np.linspace(amplitude, amplitude, 1):
        for per in np.linspace(6.0, 42.0, 361):
            for shift_v in np.linspace(12.0, 24.0, 121):
                params.append([amp, per, shift_v])
    """
    print (len(params))
    print (params[0])
    print (params[1])
    print (params[2])
    print (params[-1])
    print (type(params[0][0]))
    """

    # Read the file with the MSE values and extract the first 87,362 values:
    results = []
    for i, line in enumerate(open(mse_file, "r")):
        line = line.rstrip()
        if i == 8:                      # MSEs written in line #9!
            line = line.split("\t")
            line = [float(item) for item in line]
            results = line[43681*int(str(amplitude)[-1]):43681*(int(str(amplitude)[-1])+1)]

    """
    print (len(results))
    print (results[0])
    print (results[-1])
    print (type(results[0]))
    """

    # Make data on 'x' & 'y' axes by using a meshgrid:
    period = np.linspace(6.0, 42.0, 361)
    shiftv = np.linspace(12.0, 24.0, 121)
    X, Y = np.meshgrid(period, shiftv)

    """
    print (X)
    print (X.shape)
    print (len(X))
    print (Y)
    print (Y.shape)
    print (len(Y))
    """

    # Extract the data with locked amplitude:
    def Find_MSE(per, sft):
        for item, mse in zip(params, results):
            if item[0] == amplitude and item[1] == per and item[2] == sft:
                return mse

    Z = [[0 for i in range(X.shape[1])] for j in range(X.shape[0])]
    for index_row, (row_x, row_y) in enumerate(zip(X, Y)):
        for index_column, (column_x, column_y) in enumerate(zip(row_x, row_y)):
            mse_value = Find_MSE(per=column_x, sft=column_y)
            #print ("Index_Row = {}".format(index_row))
            #print ("Index_Col = {}".format(index_column))
            Z[index_row][index_column] = mse_value


    Z = np.matrix(Z)
    """
    print (Z)
    print (Z.shape)
    print (len(Z))
    """

    # Plot:
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_title('MSE Surface Plot with Locked Amp = {}'.format(amplitude))
    ax.set_xlabel('X = Period')
    ax.set_ylabel('Y = Shift_v')
    ax.set_zlabel('Z = MSE')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    #ax.view_init(elev=elev, azim=35)

    plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE_Surface_Amp_{}.png"
                .format(amplitude), bbox_inches="tight")
    plt.show()
    plt.close()


for i in [2.0, 2.1, 2.2]:
    PlotSurfaceMSE(amplitude=i)
    print ("Done for {}!".format(i))