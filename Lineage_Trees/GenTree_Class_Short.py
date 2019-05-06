# ----- LineageTree Creator CLASS-----

# ----- File & Table have much less data in them: ['Cell_ID', 'Frm[0]', 'Frm[-1]', 'CCT[m]', 'CCT[h]', 'Gen#']

import time
start_time = time.process_time()

class ProcessTrackedMovies:

    def __init__(self, pos=8, data_date='17_07_31', exp_type='MDCK_WT_Pure', user='Kristina'):

        # Initialise the entry file arguments as self.variables:
        self.pos = str(pos)
        self.data_date = data_date
        self.exp_type = exp_type
        self.user = user

        # Choose directory from which you want to import xml_file:
        #self.xml_file = "/Volumes/lowegrp/Data/{}/{}/{}/pos{}/tracks/tracks_type1.xml"\
        #    .format(self.user, self.exp_type, self.data_date, self.pos)
        self.xml_file = "/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml"  # absolute directory from my Mac


    def GetCellDetails(self, cell_ID):
        """ Get the details of each cell ID once segmented & tracked.
        Args:
            cell_ID = integer, the cell of interest
            xml_file = (for now) string, absolute directory to the file from which you want the information.

        Return:
            cell_ID, file_name, node_order, isRoot, isLeaf, frameAppears, frameDisappears,
                cellcycletime_mins, cellcycletime_hrs, generation, progeny, started_as, ceased_by (all items are strings)

        Notes:
            Still plenty of adjustments to make.
            TODO: 'how_much_progeny' = Change these variables to 'member of branch with X generations'
                e.g. cell_ID 11388 is in generation 3 but is a member of 6-generational tree,
                i.e has 3 layers of ancestors and 3 layers of offspring.
            TODO: Logical checks - raise Exceptions!

            """

        self.cell_ID = cell_ID

        # When processing a long sequence of cell_IDs, print a checkpoint note once in every 100:
        if self.cell_ID % 100 == 0:
            current_time_s = round(time.process_time() - start_time, 2)
            current_time_m = round(current_time_s / 60, 2)
            current_time_h = round(current_time_m / 60, 2)
            print ("Currently Processing Cell_ID # {}... Time of computation: {} seconds = {} minutes = {} hours"
                   .format(self.cell_ID, current_time_s, current_time_m, current_time_h))

        # Create the Lineage Trees using lineage.py module:
        from lineage import LineageTreeNode, LineageTree, LineageTreePlotter
        t = LineageTree.from_xml(self.xml_file)
        self.trees = t.create()

        # Define output variables:
        node_order = None
        frameAppears = None
        frameDisappears = None
        cellcycletime_m = None
        cellcycletime_h = None
        generation = None

        # Loop through the trees to locate your cell_ID of interest:
        for node_order, tree in enumerate(self.trees):
            self.node = Traverse_Trees(cell_ID=self.cell_ID, tree=tree)

            # Pull out all necessary information from the 'node' object:
            if self.node is not None:
                    # First frame the cell appears in:
                frameAppears = self.node.start
                    # Last frame the cell appears in:
                frameDisappears = self.node.end
                    # Cell cycle time (from division to division) -> not always!
                cellcycletime_m = (self.node.end - self.node.start) * 4
                cellcycletime_h = round(cellcycletime_m / 60, 2)
                    # Generation:
                generation = self.node.depth

        if node_order is None:
            print ("Cell_ID {} not mapped to any LineageTreeNode. The label {} probably doesn't exist." \
                   .format(self.cell_ID, self.cell_ID))

        return self.cell_ID, frameAppears, frameDisappears, cellcycletime_m, cellcycletime_h, generation


    def PrintDetailsTable(self, cell_ID_list):
        """ Prints a simple ASCII-format table (https://pypi.org/project/texttable/) of details for specific cell_ID (=row):

        Details:
            header = cell_ID [0], frm[0] [1], frm[-1] [2], cct_mins [3], cct_hrs [4], generation [5]
        Args:
            cell_ID_list: list of integers, can also do 'range(start, stop)'
            TODO: How come this not need list(range(start, stop))?
        Return:
            None
            Prints the table in the console. """

        self.cell_ID_list = cell_ID_list
        call = ProcessTrackedMovies()       #TODO: Do I need to call the function in the class?

        # Initialise the table with the header:
        from texttable import Texttable  # creates simple ASCII tables
        table = Texttable(max_width=0)

        header = ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen#"]
        table.header(header)

        cols_align = ["r"] * len(header)
        table.set_cols_align(cols_align)

        # Add individual lines to the growing table, one by one:
        for i in self.cell_ID_list:
            cell_ID, frm0, frm1, cct_m, cct_h, gen = call.GetCellDetails(cell_ID = i)
            details = [str(item) for item in [cell_ID, frm0, frm1, cct_m, cct_h, gen]]
            table.add_row(details)

        # Visualise the table:
        print(table.draw())


    def StoreDetailsFile(self, cell_ID_list, file_name_suffix=None):
        """ Creates a .txt file to store details for specific ID:

        File_name:
            save_to_directory + Analysis-{}-Pos{}.txt (data_date, pos)

        File_structure:
            line[0]     = header
            line[1...n] = cell_ID details
            line[-2]    = blank line
            line[-1]    = list of non-existent cell_IDs

        Args:
            cell_ID_list: list of integers, if calling 'range', type 'list(range(start, stop))'
            file_name_suffix: add a 'label' to naming the selection of cell the file contains.
                - good to make sure the file doesn't overwrite itself by each function calling.
                - set to 'None' by default.
        Return:
            None
            Opens, writes and closes the .txt file. """

        self.cell_ID_list = cell_ID_list
        call = ProcessTrackedMovies()

        if file_name_suffix is not None:
            file_name_suffix = "_" + str(file_name_suffix)

        save_to_directory = '/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/'
        self.txt_file = open(save_to_directory + 'Analysis-{}-Pos{}'.format(self.data_date, self.pos)
                        + file_name_suffix + '.txt', 'w')

        # Create & write the header:
        header = ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#"]
        header_string = ''
        for item in header:
            header_string += item + "\t"
        header_string = header_string[:-1]
        header_string += "\n"
        self.txt_file.write(header_string)

        # Create & write the details - make sure to write one by one!
        not_exist_cell_ID = []
        for i in cell_ID_list:
            detail_string = ''
            cell_ID, frm0, frm1, cct_m, cct_h, gen = call.GetCellDetails(cell_ID = i)
            if frm0 is None or frm1 is None or cct_m is None or cct_h is None or gen is None:
                not_exist_cell_ID.append(i)
            else:
                temp_list = [str(item) for item in [cell_ID, frm0, frm1, cct_m, cct_h, gen]]
                for item in temp_list:
                    detail_string += item + "\t"
                detail_string = detail_string[:-1]
                detail_string += "\n"
                self.txt_file.write(detail_string)

        # Add list of cell_IDs which do not exist to the end & close the file.
        self.txt_file.write("\nList of cell_IDs not found in any tree: " + str(not_exist_cell_ID) + "\n")
        self.txt_file.close()
        total_time_s = round(time.process_time() - start_time, 2)
        total_time_m = round(total_time_s / 60, 2)
        total_time_h = round(total_time_m / 60, 2)
        print("Txt file closed ... Total time of computation: {} seconds = {} minutes = {} hours"
              .format(total_time_s, total_time_m, total_time_h))


def Traverse_Trees(cell_ID, tree):        # define the recursive function
    if cell_ID == tree.ID:
        return tree
    if tree.leaf is True:
        return None
    else:
        left = Traverse_Trees(cell_ID, tree.children[0])
        right = Traverse_Trees(cell_ID, tree.children[1])
        if left is not None:
            return left
        else:
            return right
