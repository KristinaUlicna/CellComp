# # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                 #
# ----- LineageTree : Raw TxtFile Processor ----- #
#                                                 #
# ----- Creator :           Kristina ULICNA ----- #
#                                                 #
# ----- Last Updated :        20th Sep 2019 ----- #
#                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # #


def FilterRawTxtFile(raw_file, trimming_limit=75):
    """ Trims (excludes) all cell_IDs which appear for the movie for less or equal to 120 minutes = 75 frames.
        Sorts the included cell_IDs numerically in ascending order & writes non-root and non-leaf cells.

    Args:
       trimming_limit (int)    -> thresfold for lifetime of cell_ID to be included in the filtered folder.
                                            Default = 75 (in frames) i.e. * 4 min increments = 300 mins = 5 hours
    Return:
        None.
        Writes the file into the designated directory.

    Note:
        Header:     ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]

    """

    filtered_file = raw_file.replace("raw", "filtered")
    filtered_file = open(filtered_file, 'w')

    line_list = []

    # Trim the short cell_IDs:
    for line in open(raw_file, 'r'):
        line = line.rstrip().split("\t")
        if len(line) == 8:
            # Write the header into the file:
            if line[0] == 'Cell_ID':
                header_string = ""
                for item in line:
                    header_string += item + "\t"
                header_string = header_string[:-1] + "\n"
                filtered_file.write(header_string)
            else:
                if float(line[3]) > trimming_limit * 4:
                    if line[6] == "False" and line[7] == "False":
                        line_list.append(line)

    # Sort the lines numerically according to the cell_ID:
    for mini_list in line_list:
        mini_list[0] = int(mini_list[0])
    line_list = sorted({tuple(x): x for x in line_list}.values())

    # Iterate through this list to only include non-root & non-leaf cells:
    for line in line_list:
        string = ""
        for item in line:
            string += str(item) + "\t"
        string = string[:-1] + "\n"
        filtered_file.write(string)
    filtered_file.close()