# ----- LineageTree Creator -----

def GetCellDetails(cell_ID, pos, data_date='17_07_31', type='MDCK_WT_Pure', user='Kristina'):
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

    # When processing a long sequence of cell_IDs, print a checkpoint note once in every 100:
    if cell_ID % 100 == 0:
        print ("Processing cell_ID {}".format(cell_ID))

    # Choose directory from which you want to import the data in xml_format:
    #xml_file = "/Volumes/lowegrp/Data/{}/{}/{}/pos{}/tracks/tracks_type1.xml".format(user, type, data_date, pos)
    xml_file = "/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml"    # absolute directory from my Mac

    # Create the Lineage Trees using lineage.py module:
    from lineage import LineageTreeNode, LineageTree, LineageTreePlotter
    t = LineageTree.from_xml(xml_file)
    trees = t.create()

    # Define output variables:
    file_name = "{}/pos{}".format(data_date, pos)
    node_order = None
    isRoot = None
    isLeaf = None
    frameAppears = None
    frameDisappears = None
    cellcycletime_mins = None
    cellcycletime_hrs = None
    generation = None
    progeny = None
    started_as = None
    ceased_by = None

    # Loop through the trees to locate your cell_ID of interest:
    for order, tree in enumerate(trees):
        node = Traverse_Trees(cell_ID=cell_ID, tree=tree)

        # Pull out all necessary information from the 'node' object:
        if node is not None:
                # Node order in the list of created trees (to be able to index if necessary):
            node_order = order
                # IsRoot?
            if node.depth == 0:
                isRoot = True
            if node.depth >= 1:
                isRoot = False
                # IsLeaf?
            isLeaf = node.leaf
                # First frame the cell appears in:
            frameAppears = node.start
                # Last frame the cell appears in:
            frameDisappears = node.end
                # Cell cycle time (from division to division) -> not always!
            cellcycletime_mins = (node.end - node.start) * 4
            cellcycletime_hrs = round(cellcycletime_mins / 60, 2)
                # Generation:
            generation = node.depth
                # How much progeny does the cell have in the movie (-1 because not counting itself!)?
            progeny = Traverse_Node_To_End(node=node) - 1

                # Read_XML file to find out the state <class> of the cell:
            started_as = 'no clue...'
            if int(frameAppears) == 0 and int(node.depth) == 0:     # if it's a root cell...
                started_as = 'originally seeded'
            if int(frameAppears) != 0 and int(node.depth) == 0:
                started_as = 'migrated into FOV'
            if int(frameAppears) != 0 and int(node.depth) >= 1:
                started_as = 'cell just divided'

            #TODO: How do I find the max number of frames in the movie?
            last_frame = 1196         #TODO: watch out for hard-coding!
            _, _, isApoptotic = ReadXMLforClass(cell_ID=cell_ID, xml_file=xml_file)

            ceased_by = 'no clue...'
            if int(frameDisappears) == last_frame and isLeaf is True:
                ceased_by = 'remains until end'
            if int(frameDisappears) != last_frame and isLeaf is False and len(node.children) == 2:
                ceased_by = 'divided by mitosis'
            if isApoptotic is True and isLeaf is True:
                ceased_by = 'died by apoptosis'

    if node_order is None:
        print ("Cell_ID {} not mapped to any LineageTreeNode. The label {} probably doesn't exist.".format(cell_ID, cell_ID))

    return cell_ID, file_name, node_order, isRoot, isLeaf, frameAppears, frameDisappears, cellcycletime_mins, cellcycletime_hrs, generation, progeny, started_as, ceased_by


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


def Traverse_Node_To_End(node):
    if node is None:
        return 0
    if node.leaf is True:
        return 1
    left = Traverse_Node_To_End(node.children[0])
    right = Traverse_Node_To_End(node.children[1])
    return left + right + 1


def ReadXMLforClass(cell_ID, xml_file):
    import xml.etree.cElementTree as ET
    XMLtree = ET.parse(xml_file)
    root = XMLtree.getroot()

    # Find the <class> list:
    class_list = []
    for trajectory in root.findall('trajectory'):
        if int(trajectory.get('id')) == cell_ID:
            class_list = trajectory.find('class').text
            class_list = class_list.split("'")
            class_list = [item for item in class_list if len(item) > 5]     # to keep 'real' words

    # Inspect the <class> list:
    class_types = list(set(class_list))
    isApoptotic = 'apoptosis' in class_list
    #TODO: Ask Alan what is <fate> in the xml_file...?

    return class_list, class_types, isApoptotic


def PrintDetailsTable(cell_ID_list):
    """ Prints a simple ASCII-format table (https://pypi.org/project/texttable/) of details for specific cell_ID (=row):

    Details:
        cell_ID [0], xml_file [1], node_order [2], isRoot [3], isLeaf [4], frameAppears [5], frameDisappears [6],
        cellcycletime_mins [7], cellcycletime_hrs [8], generation [9], progeny [10], started_as [11], ceased_by [12]
    Args:
        cell_ID_list: list of integers, can also do 'range(start, stop)' TODO: How come this not need list(range(start, stop))?
    Return:
        None
        Prints the table in the console.

    """

    # Initialise the table with the header:
    from texttable import Texttable  # creates simple ASCII tables
    table = Texttable(max_width=0)

    header = ["Cell_ID", "XML_file", "Node#", "Root?", "Leaf?", "Frm[0]", "Frm[-1]", "CCT[m]", "CCT[h]", "Gen#", "Progeny", "Started_As", "Ceased_By"]
    table.header(header)

    cols_align = ["r"] * len(header)
    table.set_cols_align(cols_align)

    # Add individual lines to the growing table, one by one:
    for i in cell_ID_list:
        cell_ID, xml_file, node_order, isRoot, isLeaf, frameAppears, frameDisappears, cellcycletime_mins, cellcycletime_hrs, generation, progeny, started_as, ceased_as = \
            GetCellDetails(cell_ID=i, pos=8, data_date='17_07_31', type='MDCK_WT_Pure', user='Kristina')
        details = [str(item) for item in [cell_ID, xml_file, node_order, isRoot, isLeaf, frameAppears, frameDisappears, cellcycletime_mins, cellcycletime_hrs, generation, progeny, started_as, ceased_as]]
        table.add_row(details)

    # Visualise the table:
    print (table.draw())


#PrintDetailsTable([103, 1960, 7158, 11388, 11531, 11582, 12015])
#PrintDetailsTable([11388, 70, 101, 12015, 10864, 103])
#PrintDetailsTable(range(0, 10))
#TODO: How is it possible that table function takes in 'range(start, stop)' argument but the file is not?
#TODO: In file, I need to specify that it's a list(range(start, stop)) that I want to iterate over...Why?


def StoreDetailsFile(cell_ID_list, file_name_suffix=None):
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

    #TODO: This is exactly why you need the class! self.pos, self.data_date, self.type, self.user
    if file_name_suffix is not None:
        file_name_suffix = "_" + str(file_name_suffix)

    save_to_directory = '/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/'
    txt_file = open(save_to_directory + 'Analysis-17_07_31-Pos8' + file_name_suffix + '.txt', 'w')

    # Create & write the header:
    header = ["Cell_ID", "XML_file", "Node #", "Root?", "Leaf?", "Frm[0]", "Frm[-1]",
              "CCT [m]", "CCT [h]", "Gen #", "Progeny", "Started_As", "Ceased_By"]
    header_string = ''
    for item in header:
        header_string += item + "\t"
    header_string = header_string[:-1]
    header_string += "\n"
    txt_file.write(header_string)

    # Create & write the details - make sure to write one by one!
    not_exist_cell_ID = []
    for i in cell_ID_list:
        detail_string = ''
        cell_ID, xml_file, node_order, isRoot, isLeaf, frameAppears, frameDisappears, cellcycletime_mins, cellcycletime_hrs, generation, progeny, started_as, ceased_as = \
            GetCellDetails(cell_ID=i, pos=8, data_date='17_07_31', type='MDCK_WT_Pure', user='Kristina')
        temp_list = [str(item) for item in [cell_ID, xml_file, node_order, isRoot, isLeaf, frameAppears, frameDisappears, cellcycletime_mins, cellcycletime_hrs, generation, progeny, started_as, ceased_as]]
        if node_order is not None:
            for item in temp_list:
                detail_string += item + "\t"
            detail_string = detail_string[:-1]
            detail_string += "\n"
            txt_file.write(detail_string)
        else:
            not_exist_cell_ID.append(i)

    # Add list of cell_IDs which do not exist to the end & close the file.
    txt_file.write("\nList of cell_IDs not found in any tree: " + str(not_exist_cell_ID) + "\n")
    txt_file.close()


StoreDetailsFile([103, 1960, 7158, 11388, 11531, 11582, 12015], file_name_suffix='Node_8_Tree')
#StoreDetailsFile([11388, 70, 101, 12015, 10864, 103])
#StoreDetailsFile(list(range(0, 13001)), file_name_suffix='All_13000_Cells')
