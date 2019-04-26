#Define a function to plot histograms with time each cell appears in the movie.

def CalculateDivisionTime(tracks_file, base=100):
    """Creates a dictionary for each cell (to make it easily 'indexable') with the first & last frame
    where the cell appears. Dictionary outputs real frame orders, list outputs real cell cycle time
    (i.e. how long the cell was captured for in the movie) in mins. Base is the histogram bin size."""

    # Create dictionary & list of division times:
    cells_dict = {}  # key = cellID, value = first & last frame
    for line in open(tracks_file, 'r'):
        line = line.rstrip().split(',')
        if int(line[3]) not in cells_dict:
            cells_dict[int(line[3])] = [int(line[2]), None]  # in minutes
        cells_dict[int(line[3])][1] = int(line[2])
    div_time_frame = [(item[1] - item[0]) for item in list(cells_dict.values())]

    # TODO: Remove the 0 exclusion, just add four (+4) to all time points...
    # CATEGORIZE CELLS: Exclude cells which only appear in a SINGLE frame:
    div_time_real = [item * 4 for item in div_time_frame if item != 0]
    single_frame_cells = len(div_time_frame) - len(div_time_real)

    # CATEGORIZE CELLS: Round up the minimums and maximums & create bins:
    maximum = base * round(max(div_time_real) / base)
    bins = list(range(0, int(maximum), base))

    # CATEGORIZE CELLS: Loop through ALL division times to categorize into bins:
    hist_cell_count = [0] * len(bins)
    for div_time in div_time_real:
        index = 0
        while index <= len(bins) - 2:
            if int(div_time) > bins[index] and int(div_time) <= bins[index + 1]:
                hist_cell_count[index] += 1
                break
            else:
                index += 1

    # CATEGORIZE CELLS: Loop through ALL division times to categorize into bins:
    bins_crop = bins[0:9]
    hist_cell_count_crop = [0] * len(bins_crop)
    for div_time in div_time_real:
        index = 0
        while index <= len(bins_crop) - 2:
            if int(div_time) > bins_crop[index] and int(div_time) <= bins_crop[index + 1]:
                hist_cell_count_crop[index] += 1
                break
            else:
                index += 1

    return cells_dict, div_time_real, single_frame_cells, hist_cell_count, hist_cell_count_crop


def PlotDivisionTimeHist(tracks_file):
    cells_dict, div_time_real, single_frame_cells, hist_cell_count, hist_cell_count_crop = CalculateDivisionTime(tracks_file)
    import matplotlib.pyplot as plt
    #fig, axs = plt.subplots(1, 1, tight_layout=True)
    plt.title("Histogram of cell cycle times captured by S&T'd movies")
    plt.hist(div_time_real, bins=len(hist_cell_count))
    # TODO: Add an hour-x-axis below the minute-x-axis.
    plt.ylim(-100)
    plt.show()
    plt.close()



PlotDivisionTimeHist('/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracks_pos2_ID_sorted.csv')
PlotDivisionTimeHist('/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracks_pos1_ID_sorted.csv')
PlotDivisionTimeHist('/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracks_pos0_ID_sorted.csv')
