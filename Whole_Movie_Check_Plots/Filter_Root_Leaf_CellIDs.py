# TODO: Filter all cells which are either roots or leaves in their lineage trees
# How would you know? Because those cell_IDs would be in the gen_0 or gen_last
# i.e would have no parent or no children -> scored 'False' & 'False' in the txt_file.


def FilterRootLeafCellIDs(txt_file):
    """ Create a new .txt file which will only contain those cell_IDs which have both a parent and 2 children,
        i.e. are not roots nor leaves in their respective lineage trees.

    Args:
        txt_file (string) -> absolute directory to a SORTED .txt file from which info is to be extracted

    Return:
        None.
        Txt file ending with suffix '_filtered.txt'.
    """

    # Open new, 'filtered' file -> replace 'sorted.txt' from file name string to '_filtered.txt':
    filtered_file = txt_file.split("_sorted")[0] + "_filtered.txt"
    filtered_file = open(filtered_file, "w")

    # Iterate the old, non-filtered file to find non-root & non-leaf cells:
    for line in open(txt_file, "r"):
        line = line.rstrip().split("\t")
        if len(line) == 8:                  # removes line 'artifacts'
            # Filter for either header OR two conditions together (given by parentheses):
            if line[0] == "Cell_ID" or (line[6] == "False" and line[7] == "False"):
                string = ""
                for item in line:
                    string += str(item) + "\t"
                string = string[:-1]
                string += "\n"
                filtered_file.write(string)

    # Close the newly-written, filtered file:
    filtered_file.close()
