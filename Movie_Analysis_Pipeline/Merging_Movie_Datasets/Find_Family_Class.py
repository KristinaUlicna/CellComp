class FindFamily(object):
    """ Class that will have 3+ functions to find the following for each cell_ID:
        - root, parent, sibling
    Args:
        cell_ID (integer)           ->      cell whose family you want to find
        filtered_file (string)      ->      the file from which you are extracting input info (e.g. cell_ID labels)
                                            - can be 'cellIDdetails_merged.txt' as well
    Return:
        [ID, CCT, gen] (list)       ->      list of found cell info: it's ID (root_ID, parent_ID or sibling_ID) - int
                                                                     it's cell cycle duration [hours] - float / string
                                                                     ("NaN" if root or leaf cell)
                                                                     it's generation (depth in the lineage tree) - int
    Notes:
        TODO: Remove the print statements!
        TODO: Tidy up the functions! FindCousins is not ready!
        TODO: You have a lot of redundancy in the functions (e.g. filtered file only contains non-root cells...)
    """

    def __init__(self, cell_ID, filtered_file):

        if "merged" in filtered_file:
            exp_type = filtered_file.split("/")[-2]
            cell_name = str(cell_ID).split("-")
            date = cell_name[-1]
            pos = cell_name[-2]
            self.cell_ID = int(cell_name[-3])
            self.filtered_file = "/Volumes/lowegrp/Data/Kristina/{}/{}/{}/analysis/cellIDdetails_filtered.txt" \
                                 .format(exp_type, date, pos)
            self.raw_file = "/Volumes/lowegrp/Data/Kristina/{}/{}/{}/analysis/cellIDdetails_raw.txt" \
                            .format(exp_type, date, pos)
        else:
            self.cell_ID = cell_ID
            self.filtered_file = filtered_file
            self.raw_file = filtered_file.replace("filtered", "raw")


    def FindItself(self):
        """ Find the details for the cell_ID itself: iterate the filtered file."""

        cell_info = []
        for line in open(self.filtered_file, "r"):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date" or len(line) < 8:
                continue
            if "-" in line[0]:
                line[0] = line[0].split("-")[0]
            if int(line[0]) == self.cell_ID:
                cell_info = [int(line[0]), float(line[4]), int(line[5])]
                return cell_info

        if not cell_info:
            print ("Warning! Cell_ID {} is not present in the filtered file.".format(self.cell_ID))
            return [None, None, None]


    def FindRoot(self):
        """ Finds the root of the tree so that you can plot the tree easily. """

        cell_info = FindFamily(cell_ID=self.cell_ID, filtered_file=self.filtered_file).FindItself()

        if cell_info[2] == 0:       # if the query cell is a root itself, return it's details, otherwise search for root
            print("Warning, query cell_ID {} is a root itself!".format(self.cell_ID))
            return cell_info
        else:
            finding = False
            for line in open(self.raw_file, "r"):
                line = line.rstrip().split("\t")
                if line[0] == "Cell_ID" or len(line) < 8:
                    continue
                if int(line[0]) == self.cell_ID:
                    finding = True                               # from this moment, mark the gen# & look for the match!
                if finding is True and int(line[5]) == 0:
                    return [int(line[0]), "NaN", int(line[5])]   # root (=gen#0) will always have unknown doubling time!


    def FindParent(self):
        """ Finds the parent (i.e. cell_ID one generation above) of the desired cell. """

        cell_info = FindFamily(cell_ID=self.cell_ID, filtered_file=self.filtered_file).FindItself()

        if cell_info[2] == 0:  # if the query cell is a root itself, return it's details, otherwise search for root
            print ("Warning, query cell_ID {} is a root - it doesn't have a parent!".format(self.cell_ID))
            return [None, None, None]
        else:
            finding = False
            for line in open(self.raw_file, "r"):
                line = line.rstrip().split("\t")
                if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date" or len(line) < 8:
                    continue
                if int(line[0]) == cell_info[0]:
                    finding = True
                    generation = int(line[5])
                if finding is True and int(line[5]) == generation - 1:
                    # Condition to return doubling time only if parent is not root nor leaf cell:
                    if generation > 1 and line[7] == "False":
                        return [int(line[0]), float(line[4]), int(line[5])]
                    else:
                        return [int(line[0]), "NaN", int(line[5])]


    def FindSibling(self):
        """ Finds the parent (i.e. cell_ID one generation above)
            & looks for the sister cell (i.e. the parent's other child)
            on the same depth as the desired cell. """

        cell_info = FindFamily(cell_ID=self.cell_ID, filtered_file=self.filtered_file).FindItself()
        parent_info = FindFamily(cell_ID=self.cell_ID, filtered_file=self.filtered_file).FindParent()

        # Read the same file in REVERSED order:
        finding = False
        for line in reversed(list(open(self.raw_file, "r"))):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date" or len(line) < 8:
                continue
            if int(line[0]) == parent_info[0]:
                finding = True
                generation = int(line[5])
            if finding is True and int(line[5]) == generation + 1 and int(line[0]) != cell_info[0]:
                if line[7] != "True":                       # if cell is not leaf
                    return [int(line[0]), float(line[4]), int(line[5])]
                else:
                    return [int(line[0]), "NaN", int(line[5])]


    def FindGrandparent(self):
        """ Only works if gen #3 or above. """

        cell_info = FindFamily(cell_ID=self.cell_ID, filtered_file=self.filtered_file)
        cell_info = cell_info.FindItself()

        if cell_info == [None, None, None]:
            return [None, None, None]
        elif cell_info[2] < 3:
            print("Warning, query cell_ID {} is in gen #{} - it doesn't have a grandparent!".format(self.cell_ID, cell_info[2]))
            return [None, None, None]
        else:
            for line in open(self.raw_file, "r"):
                line = line.rstrip().split("\t")
                if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date" or len(line) < 8:
                    continue
                if "-" in line[0]:
                    line[0] = line[0].split("-")[0]
                # Find the 'grandmother' cell = cell 2 generations up:
                if int(line[0]) == self.cell_ID:
                    parent_info = FindFamily(cell_ID=self.cell_ID, filtered_file=self.filtered_file).FindParent()
                    parent = int(parent_info[0])
                    grandparent_info = FindFamily(cell_ID=parent, filtered_file=self.filtered_file).FindParent()
                    return grandparent_info


    def FindCousins(self):
        """ Find all the cousins of the cells: 0 (min) up to 2 (max).
            Cousin = cell in the same generation
            which is not a sibling of the specific cell. """

        grandparent_info = FindFamily(cell_ID=self.cell_ID, filtered_file=self.filtered_file)
        grandparent_info = grandparent_info.FindGrandparent()

        if grandparent_info == [None, None, None]:
            return [None, None, None]
        else:
            for line in open(self.raw_file, "r"):
                line = line.rstrip().split("\t")
                if line[0] == "Cell_ID" or line[0] == "Cell_ID-posX-date" or len(line) < 8:
                    continue
                if "-" in line[0]:
                    line[0] = line[0].split("-")[0]
                # TODO: cousins only present in gen #3 & above - finish function:
        return ["To be updated"]



# Call the class as follows:
"""
cell_list = [3011, 3040, 5204, 1804, 2654, 8713, 3514, 8710]
root_list = []
parent_list = []
sibling_list = []
grandparent_list = []
cousin_list = []

txt_file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos6/cellIDdetails_filtered.txt"
for cell_ID in cell_list:
    call = FindFamily(cell_ID=cell_ID, filtered_file=txt_file)
    root_list.append(call.FindRoot())
    parent_list.append(call.FindParent())
    sibling_list.append(call.FindSibling())
    grandparent_list.append(call.FindGrandparent())
    cousin_list.append(call.FindCousins())

print ("Query Cell:\t{}".format(cell_list))
print ("Tree Root:\t{}".format(root_list))
print ("Parent:\t\t{}".format(parent_list))
print ("Sibling:\t{}".format(sibling_list))
print ("Grandpa:\t{}".format(grandparent_list))
print ("Cousins:\t{}".format(cousin_list))

"""