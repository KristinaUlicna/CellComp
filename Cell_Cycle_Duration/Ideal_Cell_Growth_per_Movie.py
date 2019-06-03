import matplotlib.pyplot as plt

# TODO: Calculate the 'off-factor'
# = how many cellIDs should I have per movie in total,
# considering the starting number of cells?


def PlotIdealCellGrowth():
    """ Plot an 'ideal' growth curve for MDCK cells with variable cell cycle duration & starting cell amount. """

    # Make vectors:
    def MakeVectors(cells_start, doubling_time):
        movie_time = 80
        cell_list = [cells_start]
        time_list = [0]

        while time_list[-1] < movie_time:
            cell_list.append(cell_list[-1] * 2)
            time_list.append(time_list[-1] + doubling_time)

        return (cell_list, time_list)

    # Initiate the figure:
    fig = plt.figure()
    plt.xlabel("Time [hours]")
    plt.ylabel("Cell count")
    plt.title("Ideal Cell Growth per movie")

    # Plot the dependencies:
    cells_start = [120, 140, 160, 180, 200]
    doubling_time = [16, 18, 20, 22, 24]

    for i in cells_start:
        for j in doubling_time:
            cell_list, time_list = MakeVectors(cells_start=i, doubling_time=j)
            plt.plot(time_list, cell_list, "-o", label="{} cells; {} hrs".format(i, j))
    plt.legend(loc="upper left")
    plt.show()
    plt.close()


PlotIdealCellGrowth()