from operator import itemgetter

def SortCellIDFile(txt_file):
    """ Sorts the file by the first column -> int(line[0]) <- in numerical order.

    Args:
        txt_file (should end with 'cellIDdetail_raw.txt') -> input; unsorted file.

    Return:
        None.
        Writes a new, sorted 'cellIDdetail_sorted.txt' file into the same directory.

    Details:
        ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"].

    """

    # Read the txt_file & divide into header & lines to be sorted:
    header_list = []
    line_list = []

    for line in open(txt_file, 'r'):
        line = line.rstrip().split("\t")
        if len(line) == 8:
            if line[0] == 'Cell_ID':
                header_list = line
            else:
                line[0] = int(line[0])
                line_list.append(line)

    # Write the 'cellIDdetails_sorted.txt' file & type the header:
    sorted_file = txt_file.split("/")[:-1]
    sorted_file = '/'.join(sorted_file) + "/cellIDdetails_sorted.txt"

    file = open(sorted_file, 'w')
    header_string = ''
    for item in header_list:
        header_string += item + "\t"
    header_string = header_string[:-1]
    header_string += "\n"
    file.write(header_string)

    # Sort the lines numerically according to the cell_ID, write & close:
    for line in sorted(line_list, key=itemgetter(0)):
        string = ''
        for item in line:
            string += str(item) + "\t"
        string = string[:-1]
        string += "\n"
        file.write(string)
    file.close()
