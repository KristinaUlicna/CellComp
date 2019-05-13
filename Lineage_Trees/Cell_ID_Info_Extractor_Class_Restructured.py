# # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                 #
# ----- LineageTree : CellID Info Extractor ----- #
#                                                 #
# ----- Creator :       Kristina ULICNA     ----- #
#                                                 #
# ----- Last Updated :  13th May 2019       ----- #
#                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # #


# Import all the necessary libraries:
from lineage import LineageTreeNode, LineageTree, LineageTreePlotter
from texttable import Texttable  # creates simple ASCII tables

import os
import shutil       # does the same as 'os.rename(old_file, new_file)' but if directories have different structures
import time
start_time = time.process_time()


class GetCellDetails():
    """ Store relevant details of each cell_ID in the xml_file (=output of tracking & segmentation with classification).
        Uses recursive function to iterate over trees created using lineage.py module.
        Relevant cell_ID details which are processed are listed in the 'header' variable.

    Args:
        version: (integer)              -> specify which tracks_type1.xml you want to use as source.
        server_ON: (False by default)   -> change to True if using server to read & write files.
        pos, data_date, exp_type, user  -> to navigate the server to the correct folders/files.

    Return:
        Writes a .txt file as an output.        default = True
        Prints an ASCII table as an output.     default = False

    Notes: To iterate over the class calling, re-open the file for appending with 'a' mode to write into it.

    """

    def __init__(self, xml_file=None, version=0, server_ON=False, pos=8, data_date='17_07_31', exp_type='MDCK_WT_Pure', user='Kristina'):

        if xml_file is not None:
            xml_file_name = str(xml_file)
            xml_file_name = xml_file_name.split("/")
            self.pos = xml_file_name[-3].split('pos')[-1]
            self.data_date = xml_file_name[-4]
            self.exp_type = xml_file_name[-5]
            self.user = xml_file_name[-6]
            self.server_ON = True
        else:
            self.pos = str(pos)
            self.data_date = data_date
            self.exp_type = exp_type
            self.user = user
            self.server_ON = server_ON
            self.version = str(version)

        self.table = Texttable(max_width=0)
        self.txt_file = open("/Users/kristinaulicna/Documents/Rotation_2/temporary.txt", 'w')


    def IterateTrees(self, write_file = True, print_table = False):

        # Choose directory from which you want to import xml_file:
        # TODO: Are you sure this will work? Don't you need shutil instead of os?
        if self.server_ON:
            xml_file = "/Volumes/lowegrp/Data/{}/{}/{}/pos{}/tracks/tracks_type1.xml" \
                        .format(self.user, self.exp_type, self.data_date, self.pos)
        else:
            xml_file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracker_Updates_XML_Files/" \
                       "ver{}/tracks_type1_ver{}.xml".format(self.version, self.version)

        # What information do you want to store?
        header = ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]

        # Create the Lineage Trees using lineage.py module:
        t = LineageTree.from_xml(xml_file)
        trees = t.create()

        if write_file is True:

            # Initialise the file & write the header:
            header_string = ''
            for item in header:
                header_string += item + "\t"
            header_string = header_string[:-1]
            header_string += "\n"
            self.txt_file.write(header_string)

            # Loop through the trees:
            for node_order, tree in enumerate(trees):
                Traverse_Trees(tree=tree, write_file=write_file, print_table=print_table)

            # Rename the file, close it & print the time of processing:
            if self.server_ON:
                #TODO: mkdir
                server_dir = "/Volumes/lowegrp/Data/{}/{}/{}/pos{}/tracks/analysis/" \
                    .format(self.user, self.exp_type, self.data_date, self.pos)
                if not os.path.exists(server_dir):
                    os.makedirs(server_dir)
                new_file_name = open(server_dir + "/cellIDdetails.txt", "w")

            else:
                new_file_name = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracker_Updates_XML_Files/" \
                                "ver{}/cellIDinfo_ver{}.txt".format(self.version, self.version)

            old_file_name = str(self.txt_file).split("'")[1]
            shutil.move(old_file_name, new_file_name)

        self.txt_file.close()


def Traverse_Trees(tree, write_file, print_table):        # define the recursive function

    # Initialise the variables:
    cell_ID = tree.ID
    frm_st = int(tree.start)
    frm_en = int(tree.end)
    cct_m = (int(tree.end) - int(tree.start)) * 4
    cct_h = round(float(cct_m / 60), 2)
    gen = int(tree.depth)
    is_root = True if tree.depth == 0 else False
    is_leaf = tree.leaf
    details = [str(item) for item in [cell_ID, frm_st, frm_en, cct_m, cct_h, gen, is_root, is_leaf]]

    # Write into the file:
    if write_file is True:
        txt_file = open("/Users/kristinaulicna/Documents/Rotation_2/temporary.txt", 'a')
        detail_string = ''
        for item in details:
            detail_string += item + "\t"
        detail_string = detail_string[:-1]
        detail_string += "\n"
        txt_file.write(detail_string)

    # Print into the table:
    if print_table is True:
        table.add_row(details)
        print(table.draw())

    # Check if the current node your just processed branches further:
    if tree.leaf is False:
        Traverse_Trees(tree.children[0], write_file, print_table)
        Traverse_Trees(tree.children[1], write_file, print_table)


#print("Txt file closed ... Total time of computation: {} seconds"
#        .format(round(time.process_time() - start_time, 2)))
