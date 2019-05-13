from operator import itemgetter

def SortCellIDFile(txt_file):
    """ Sorts the file by the first column -> int(line[0]) <- in numerical order by overwriting the file.
        Insert the file name (end with .txt) with absolute directory. """

    # Read the txt_file & divide into header & lines to be sorted:
    header_list = []
    line_list = []
    for line in open(txt_file, 'r'):
        line = line.rstrip().split("\t")
        if line[0] == 'Cell_ID':
            header_list = line
        else:
            line[0] = int(line[0])
            line_list.append(line)

    # Re-write the file & type the header:
    file = open(txt_file, 'w')
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


SortCellIDFile("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Analysis-17_07_31-Pos8_All_Cells_ver4.txt")