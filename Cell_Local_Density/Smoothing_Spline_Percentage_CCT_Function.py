# TODO: Smooth the density of each individual cell.
# TODO: Approximate the density at timepoints between 1 to 100 %.
# TODO: Write into a new file.

import yaml
import time
from scipy.interpolate import UnivariateSpline


def SmoothDensity(density_dict_txt_file):
    """ Function to smooth the density of each individual cell.
        Approximate the density at timepoints between 1 to 100 %.
        Write into a new .txt file

    Args:
        density_dict_txt_file (str) -> absolute path to the dictionary produced for density values per cell_ID.
            'header' = cell_ID followed by a hundred values for density...

    Return:
        None.
        Writes the .txt file and stores relevant info.
    """

    # According to the input file (=density_dict_txt_file), open the 'cellIDdetails_filtered.txt' file
    dir = density_dict_txt_file.split("/")
    dir = "/".join(dir[:-2]) + "/"
    cellIDdetails_filtered_file = dir + "/analysis/cellIDdetails_filtered.txt"

    # Create a list of relevant cell IDs for which you demand the density smoothing to be done:
    cell_ID_list = []
    cct_hrs_list = []
    for line in open(cellIDdetails_filtered_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Cell_ID":
            cell_ID_list.append(line[0])
            cct_hrs_list.append(line[4])
    print ("Density data are being calculated for {} cell IDs.".format(len(cell_ID_list)))

    # Write new file & initialise it with a header:
    density_output_txt_file = dir + "/density/cellID_density_smoothed.txt"
    density_output_txt_file = open(density_output_txt_file, "w")
    header = ["Cell_ID", "CCT[h]"] + [str(item)+"%" for item in range(1, 101, 1)]
    header_string = ''
    for item in header:
        header_string += str(item) + "\t"
    header_string = header_string[:-1] + "\n"
    density_output_txt_file.write(header_string)

    # Read raw data from the input file & create a dictionary out of them:
    start_time = time.process_time()
    dictionary = {}
    for string in open(density_dict_txt_file, "r"):
        dictionary = yaml.load(string)
        print("String -> Dictionary (len = {}): {} in {} minutes."
              .format(len(dictionary), type(dictionary), round((time.process_time() - start_time) / 60, 2)))

    # Read the dictionary to extract frame data and density data into lists:
    index = 0
    for cell_ID, value in dictionary.items():
        if str(cell_ID) in cell_ID_list:

            # Create vectors:
            frame_list = []
            density_list = []
            for frame in value:
                frame_list.append(int(frame[0]))
                density_list.append(float(frame[1]))

            # Check there is enough data (i.e. the cell ID is not an artifact) to do the operation:
            if len(frame_list) <= 3 or len(density_list) <= 3:
                print ("\tNot enough data to instantiate a univariate spline. Cell ID {} not processed further."
                       .format(cell_ID))
                continue

            # Smooth the data for each cell_ID (=key) here:
            s = UnivariateSpline(x=frame_list, y=density_list, s=1)

            # Extend / Shrink cell's lifetime to 100% (=100 datapoints):
            xs = [item * 100 for item in frame_list]
            step = (frame_list[-1] - frame_list[0] + 1)
            xs = list(range(xs[0], xs[-1], step))
            xs = [item / 100 for item in xs]

            # Calculate the ys according to approximated density values per each x-datapoint:
            ys = s(xs)

            # Loop through the 'ys' values and write them into a file:
            string = str(cell_ID_list[index]) + "\t" + str(cct_hrs_list[index]) + "\t"
            for number in ys:
                string += str(number) + "\t"
            string = string[:-1] + "\n"
            density_output_txt_file.write(string)

            index += 1

    # Close the file after all cell_IDs have been processed:
    density_output_txt_file.close()
