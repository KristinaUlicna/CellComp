# TODO: Write a class that will have functions to find the following for each cell_ID:
#       - root, parent, sibling

class FindFamily(object):
    """ Class that will have 3+ functions to find the following for each cell_ID:
        - root, parent, sibling
    Args:
        cell_ID (integer)           ->      cell whose family you want to find
        filtered_file (string)      ->      the file from which you are extracting input info (e.g. cell_ID labels)
                                            - can be 'cellIDdetails_merged.txt' as well
    """

    def __init__(self, cell_ID, filtered_file):

        self.cell_ID = cell_ID
        self.filtered_file = filtered_file
        self.raw_file = None

        if "merged" in self.filtered_file:
            print ("Need to access raw files according cell_ID string name!")
            self.raw_file = ""
        else:
            self.raw_file = self.filtered_file.replace("filtered", "raw")


    def FindRoot(self):
        """ Finds the root of the tree so that you can plot the tree easily. """

        finding = False  # 'finding' is a marker => from this moment, look for 0 (so it doesn't return first 0 in file)
        for line in open(self.raw_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or len(line) < 8:
                continue
            if int(line[0]) == self.cell_ID:
                finding = True
            if finding is True and int(line[5]) == 0:
                return [int(line[0]), "NaN"]            # generation 0 (=root) will always have unknown doubling time!


    def FindParent(self):
        """ Finds the parent (i.e. cell_ID one generation above) of the desired cell. """

        finding = False  # 'finding' is a marker => from this moment, look for 0 (so it doesn't return first 0 in file)
        for line in open(self.raw_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or len(line) < 8:
                continue
            if int(line[0]) == int(self.cell_ID):
                finding = True
                generation = int(line[5])
            if finding is True and int(line[5]) == generation - 1:    # need to condition if parent is also root cell!
                if generation > 1:
                    return [int(line[0]), float(line[4])]
                else:
                    return [int(line[0]), "NaN"]

    def FindSibling(self):
        """ Finds the parent (i.e. cell_ID one generation above)
            & looks for the sister cell (i.e. the parent's other child)
            on the same depth as the desired cell. """

        finding = False  # 'finding' is a marker => from this moment, look for 0 (so it doesn't return first 0 in file)
        for line in open(self.raw_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or len(line) < 8:
                continue
            if int(line[0]) == int(self.cell_ID):
                finding = True
                generation = int(line[5])
            if finding is True and int(line[5]) == generation - 1:    # need to condition if parent is also root cell!
                parent = int(line[0])
                break

        # Read the same file in reversed order:
        finding = False
        for line in reversed(list(open(self.raw_file, "r"))):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or len(line) < 8:
                continue
            if int(line[0]) == parent:
                finding = True
                generation = int(line[5])
            if finding is True and int(line[5]) == generation + 1 and int(line[0]) != self.cell_ID:
                if line[7] != "True":                       # if cell is not leaf
                    return [int(line[0]), float(line[4])]
                else:
                    return [int(line[0]), "NaN"]





# Call the class as follows:

cell_list = [3040, 1804, 2654, 8713, 3514]
root_list = []
parent_list = []
sibling_list = []
txt_file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos6/cellIDdetails_filtered.txt"
for cell_ID in cell_list:
    root = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindRoot()
    root_list.append(root)
    parent = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindParent()
    parent_list.append(parent)
    sibling = FindFamily(cell_ID=cell_ID, filtered_file=txt_file).FindSibling()
    sibling_list.append(sibling)

print (cell_list)
print (root_list)
print (parent_list)
print (sibling_list)