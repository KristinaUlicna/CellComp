from operator import itemgetter

class ProcessRawTxtFile(object):
    """ 'cellIDdetails_raw.txt' = input file from iterated trees:
            -> 'cellIDdetails_trimmed.txt'
            -> 'cellIDdetails_sorted.txt'
            -> 'cellIDdetails_filtered.txt'
    Args:
        txt_file (string)   ->   'cellIDdetails_raw.txt' = input file from iterated trees

    Return:
        None.
        Writes the required files into designated directory.

    Header:
        ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]

    """

    def __init__(self, raw_file):

        self.raw_file = raw_file
        self.trimmed_file = None
        self.sorted_file = None
        self.filtered_file = None

        self.header_list = []
        self.header_string = ""
        self.line_list = []


    def TrimCellIDFile(self):
        """ Trims (excludes) all cell_IDs which appear for the movie for less or equal to 20 minutes = 5 frames.
            This is an 'informative' file. Will probably not be used for further analysis,
            but is handy for printing summary statistics for each movie. """

        # Trim the short cell_IDs:
        for line in open(self.raw_file, 'r'):
            line = line.rstrip().split("\t")
            if len(line) == 8:
                if line[0] == 'Cell_ID':
                    self.header_list = line
                    header_string = ""
                    for item in self.header_list:
                        header_string += item + "\t"
                    header_string = header_string[:-1]
                    header_string += "\n"
                    self.header_string = header_string
                else:
                    if float(line[3]) > 20:
                        self.line_list.append(line)

        # Write the 'cellIDdetails_trimmed.txt' file & type the header:
        self.trimmed_file = self.raw_file.replace("raw", "trimmed")
        file = open(self.trimmed_file, 'w')
        file.write(self.header_string)

        # Sort the lines numerically according to the cell_ID, write & close:
        for line in self.line_list:
            string = ""
            for item in line:
                string += str(item) + "\t"
            string = string[:-1]
            string += "\n"
            file.write(string)
        file.close()


    def SortCellIDFile(self):
        """ Sorts the trimmed file by the first column -> int(line[0]) <- in numerical order. """

        # Write the 'cellIDdetails_sorted.txt' file & type the header:
        self.sorted_file = self.raw_file.replace("raw", "sorted")
        file = open(self.sorted_file, 'w')
        file.write(self.header_string)

        # Check if list is not empty:
        if not self.line_list:
            raise Exception("Warning, no cell_ID lines to write (empty list) - Run TrimCellIDFile() function first!")

        # Sort the lines numerically according to the cell_ID:
        for line in self.line_list:
            line[0] = int(line[0])
        self.line_list = sorted({tuple(x): x for x in self.line_list}.values())

        # Write & close the file:
        for line in self.line_list:
            string = ""
            for item in line:
                string += str(item) + "\t"
            string = string[:-1]
            string += "\n"
            file.write(string)
        file.close()


    def FilterCellIDFile(self):
        """ Filters for root & leaf cell_IDs by only including those cell_IDs which have both 1 parent and 2 children. """

        # Check if list is not empty:
        if not self.line_list:
            raise Exception ("Warning, no cell_ID lines to write (empty list)\nRun TrimCellIDFile() function first!")

        # Check if the list has been sorted:
        if int(self.line_list[0][0]) >= int(self.line_list[1][0]):
            raise Exception("Warning, cell_ID lines are not in order\nRun SortCellIDFile() function first!")

        # Write the 'cellIDdetails_filtered.txt' file & type the header:
        self.filterd_file = self.raw_file.replace("raw", "filtered")
        file = open(self.filterd_file, 'w')
        file.write(self.header_string)

        # Iterate the old, non-filtered file to find non-root & non-leaf cells:
        for line in self.line_list:
            if line[6] == "False" and line[7] == "False":
                string = ""
                for item in line:
                    string += str(item) + "\t"
                string = string[:-1]
                string += "\n"
                file.write(string)
        file.close()
