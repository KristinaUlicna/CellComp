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
from Sequitr_Package_Scripts.lineage import *
import os
import time
start_time = time.process_time()


class GetCellDetails(object):

    """ Store relevant details of each cell_ID in the xml_file (=output of tracking & segmentation with classification).
        Uses recursive function to iterate over trees created using lineage.py module.
        Relevant cell_ID details which are processed are listed in the 'header' variable.

    Args:
        xml_file (string)    ->     absolute path to the xml_file from which you want to iterate lineage trees

    Return:
        None.
        Writes a 'cellIDdetails_raw.txt' file (output) into the /analysis/channel_XFP/ directory as the input specifies.

    Notes:
        To iterate over the class calling, re-open the file for appending with 'a' mode to write into it.

    """

    def __init__(self, xml_file):
        """ Create both paths: channel_GFP (for tracks_type1.xml) & channel_RFP (for tracks_type2.xml)
            irrespectively of which type of xml_file you are using for cell_ID info extraction. """

        # Create 'analysis' folder directory for the channel you are processing:
        directory = '/'.join(xml_file.split("/")[:-2])      # directory into ../user/exp_type/data_date/posX/

        if "tracks_type1" in xml_file:
            directory = directory + "/analysis/channel_GFP/"
        if "tracks_type2" in xml_file:
            directory = directory + "/analysis/channel_RFP/"

        if not os.path.exists(directory):
            os.makedirs(directory)
        txt_file = directory + "cellIDdetails_raw.txt"

        self.xml_file = xml_file
        self.txt_file = txt_file


    def IterateTrees(self):

        # What information do you want to store?
        header = ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]

        # Create the Lineage Trees using lineage.py module:
        t = LineageTree.from_xml(self.xml_file)
        trees = t.create()

        # Loop through the trees:
        details_list = []
        for node_order, tree in enumerate(trees):
            tree_details_list = Traverse_Trees(tree=tree)
            print (details_list)

            details_list.append(tree_details_list)
        print (details_list)

        """
        # Initialise the file & write the header:
        file = open(self.txt_file, 'w')

        header_string = ''
        for item in header:
            header_string += item + "\t"
        header_string = header_string[:-1]
        header_string += "\n"
        file.write(header_string)

        # Write the details stored as strings into the file:
        for cell_ID in details_list:
            file.write(cell_ID)

        # When looping is finished, close the still opened file:
        file.close()
        """


def Traverse_Trees(tree):        # define the recursive function

    tree_details_list = []

    # Initialise the variables:
    cell_ID = tree.ID
    frm_st = int(tree.start)
    frm_en = int(tree.end)
    cct_m = (int(tree.end) - int(tree.start)) * 4
    cct_h = round(float(cct_m / 60), 2)
    gen = int(tree.depth)
    is_root = True if tree.depth == 0 else False
    is_leaf = tree.leaf

    details = [cell_ID, frm_st, frm_en, cct_m, cct_h, gen, is_root, is_leaf]

    if not tree_details_list:
        tree_details_list = details
    else:
        tree_details_list.append(details)

    # Check if the current node your just processed branches further:

    if tree.leaf is False:
        Traverse_Trees(tree.children[0])
        Traverse_Trees(tree.children[1])

    return tree_details_list
