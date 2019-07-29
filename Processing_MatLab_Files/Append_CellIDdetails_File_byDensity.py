import sys
sys.path.append("../")

import yaml
from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths
from Processing_MatLab_Files.Finding_Density_Values import FindDensitySpan

# Import directories for all movies available:
_, txt_file_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")
# file = /Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_01_24/pos7/analysis/cellIDdetails_raw.txt

for file in sorted(txt_file_list):
    filtered_file = file.replace("raw", "filtered")
    print (filtered_file)
    density_file = file.replace("analysis/cellIDdetails_raw", "density/cellID_density")
    print (density_file)

    # Read the created dictionary from a file:
    dictionary = {}
    for string in open(density_file, "r"):
        dictionary = yaml.load(string)
    print ("Dictionary created. Length = {}".format(len(dictionary)))

    # Create a new file to write new values into:
    new_file = density_file.replace("cellID_density", "cellIDdetails_density")
    all_details_file = open(new_file, "w")
    header = ["Cell_ID", "Frm[0]", "Frm[-1]",	"CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf",
                "Den[0]", "Den[1/4]", "Den[1/2]", "Den[3/4]", "Den[-1]"]
    header_string = ""
    for item in header:
        header_string += item + "\t"
    header_string = header_string[:-1]
    header_string += "\n"
    all_details_file.write(str(header_string))
    print ("New 'cellIDdetails_density.txt' created. Header written.")

    # Loop through all the filtered cellIDs and look for their densities:
    for line in open(filtered_file, "r"):
        line = line.rstrip().split("\t")
        frame_list = []
        density_list = []
        if line[0] != "Cell_ID":
            for key, value in dictionary.items():
                if key == int(line[0]):
                    for frame in value:
                        frame_list.append(int(frame[0]))
                        density_list.append(float(frame[1]))
                    density_values = []
                    for span in ["birth", "one_quarter", "half_way", "three_quarters", "mitosis"]:
                        density_value = FindDensitySpan(density_list=density_list, span=span)
                        density_values.append(density_value)
                    print("Density values for cellID {}: {}".format(int(line[0]), density_values))

                    # Write this into a file:
                    density_values = [str(item) for item in density_values]
                    line = line + density_values
                    print ("New line with 5 density values: {}".format(line))
                    string = ""
                    for item in line:
                        string += item + "\t"
                    string = string[:-1]
                    string += "\n"
                    all_details_file.write(string)

    # Close the file:
    all_details_file.close()
    print ("Closed File {}".format(new_file))
