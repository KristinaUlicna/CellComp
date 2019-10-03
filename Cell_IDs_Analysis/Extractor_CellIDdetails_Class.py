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

import sys
sys.path.append("../")

from Sequitr_Lineage_Trees.lineage import *
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

        # Create analysis directory for both channels:
        self.xml_file = xml_file

        directory = xml_file.split("/")[:-2]      # directory into ../user/exp_type/data_date/posX/
        user, exp_type, data_date, pos = directory[-4], directory[-3], directory[-2], directory[-1]
        directory = '/'.join(directory)
        for channel in ["GFP", "RFP"]:
            analysis_directory = directory + "/analysis/channel_{}/".format(channel)
            if not os.path.exists(analysis_directory):
                os.makedirs(analysis_directory)

        #TODO: Check if movies with RFP channel only (Scribble) will output tracks_type2.xml file! If not, change below:

        if "tracks_type1" in xml_file:
            self.txt_file = directory + "/analysis/channel_GFP/cellIDdetails_raw.txt"
        if "tracks_type2" in xml_file:
            self.txt_file = directory + "/analysis/channel_RFP/cellIDdetails_raw.txt"


    def IterateTrees(self):

        # What information do you want to store?
        header = ["Cell_ID", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen_#", "IsRoot", "IsLeaf"]

        # Create the Lineage Trees using lineage.py module:
        t = LineageTree.from_xml(self.xml_file)
        trees = t.create()

        # Initialise the file & write the header:
        file = open(self.txt_file, 'w')

        header_string = ''
        for item in header:
            header_string += item + "\t"
        header_string = header_string[:-1]
        header_string += "\n"
        file.write(header_string)

        # Loop through the trees:
        for node_order, tree in enumerate(trees):
            Traverse_Trees(tree=tree, txt_file=self.txt_file)

        # When looping is finished, close the still opened file:
        file.close()


def Traverse_Trees(tree, txt_file):        # define the recursive function

    # Initialise the variables:
    cell_ID = tree.ID
    frm_st = int(tree.start)
    frm_en = int(tree.end)
    cct_m = (int(tree.end) - int(tree.start)) * 4
    cct_h = round(float(cct_m / 60), 2)
    gen = int(tree.depth)
    is_root = True if tree.depth == 0 else False
    is_leaf = tree.leaf
    if frm_st > frm_en:
        raise Exception("Warning, frameAppears ({}) > frameDisappears ({}) ! Tracking error!".format(frm_st, frm_en))
    details = [str(item) for item in [cell_ID, frm_st, frm_en, cct_m, cct_h, gen, is_root, is_leaf]]

    # Write the details into a 'cellIDdetails_raw.txt' file:
    file = open(txt_file, 'a')
    detail_string = ''
    for item in details:
        detail_string += item + "\t"
    detail_string = detail_string[:-1]
    detail_string += "\n"
    file.write(detail_string)

    # Check if the current node your just processed branches further:
    if tree.leaf is False:
        Traverse_Trees(tree.children[0], txt_file)
        Traverse_Trees(tree.children[1], txt_file)
