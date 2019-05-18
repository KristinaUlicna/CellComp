# Define function to spit out trees:

class CellParentPairs(object):

    def __init__(self, pos, data_date):
        """ Get pairs of cells which were detected to have a parent.
            Build-in checks for parent ID < cell ID (else: Warning!)
            Args:
                data_date = date of Anna's experiment (name of folder in 'MDCK_WT_Pure'); format = 'YY_MM_DD'
                pos = integer; position in the microscope
            Return:
                parent_list = list of lists with pairs of [[parentID, cellID], [...], ...], ordered ascendingly."""

        self.pos = str(pos)
        self.data_date = data_date

        # Parse through the 'tracks_type1.xml' file on the server:
        import xml.etree.ElementTree as ET
        self.tree = ET.parse("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/{}/pos{}/HDF/tracks_type1.xml".format(data_date, pos))
        #self.tree = ET.parse("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/tracks_type1.xml")
        self.root = self.tree.getroot()


    def FindCellParents(self):
        """ Get pairs of cells which were detected to have a parent. Build-in check for parent ID < cell ID (else: Warning!)
        Args:
            None.
        Return:
            parent_list = list of lists with pairs of [[parentID, cellID], [...], ...] in ascending order. """

        # Loop through all cells in the file & pick those which had a parent detected:
        counter = 0
        self.parent_list = []
        for trajectory in self.root.findall('trajectory'):
            cellID = trajectory.get('id')
            parentID = trajectory.find('parent').text
            if str(parentID) != 'None':
                #print ("CellID: {}, \tParentID {}".format(cellID, parentID))
                self.parent_list.append([int(parentID), int(cellID)])
                if int(cellID) > int(parentID):
                    counter += 1
        if counter != len(self.parent_list):
            raise Exception("Warning! The parent ID ({})  >= of cell ID ({})". format(int(parentID), int(cellID)))

        # Summarise what the program has done:
        print ("\nFile: {}\nTotal cell #: {}\t'Non-orphan' cell #: {}\tPercentage of 'non-orphan' cells: {} %" \
               .format(self.root.attrib, len(self.root), counter, round(counter*100/len(self.root), 2)))

        # Order parent_list of small_lists according to the first item value (parentID) i.e. small_list[0]:
        import operator
        self.parent_list = sorted(self.parent_list, key=operator.itemgetter(0))

        return self.parent_list


    def CheckFor2Children(self):
        """ Check basic parent_list properties:
            Does every parent cell divide into 2 new cells?
            If so, do nothing. If not, raise an Exception. """

        # Same parent's children merged together:
        self.parent_dict = {}
        for pair_list in self.parent_list:
            if pair_list[0] not in self.parent_dict:
                self.parent_dict[pair_list[0]] = [pair_list[1]]
                continue
            self.parent_dict[pair_list[0]].append(pair_list[1])

        # Checking that all parents (.keys()) have exactly 2 children (.value()):
        for key, value in self.parent_dict.items():
            self.parent_dict[key] = sorted(value)
            if len(value) != 2:
                raise Exception("Mitosis tracked incorrectly!", "'Parent': ['child', 'child'] has less or more than 2 children {}".format(len(value)))

        return self.parent_dict


    def ProgenyLabelling(self):
        """ Check the assumption that the children of parents who divide at the beginning of the movie are labelled
            with numbers closer to each other rather than cells which divide towards the end of the movie.
            Can you see any exponential relationship as the parent cell label is increasing? """

        # Use the list (not a dictionary) as an iterable - order is important here, and dicts are intrinsically not ordered!
        label_diff = []
        label_ratio = []
        parents = []
        for pair_list in self.parent_list:
            parents.append(pair_list[0])
            label_diff.append(pair_list[1] - pair_list[0])
            label_ratio.append(pair_list[1] / pair_list[0])
        parents = list(sorted(set(parents)))

        # Create left & right vectors to be plotted:
        label_diff_left = []
        label_diff_right = []
        label_ratio_left = []
        label_ratio_right = []
        for index, item in enumerate(label_diff):
            if index % 2 == 0:
                label_diff_left.append(item)
            else:
                label_diff_right.append(item)
        for index, item in enumerate(label_ratio):
            if index % 2 == 0:
                label_ratio_left.append(item)
            else:
                label_ratio_right.append(item)
        x = parents
        y1 = label_diff_left
        y2 = label_diff_right
        y3 = label_ratio_left
        y4 = label_ratio_right

        # Plot the vectors as scatter plots:
        import matplotlib.pyplot as plt

        f, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot(x, y1, color='salmon', alpha=.5, label='Left Branch')
        ax1.plot(x, y2, color='aqua', alpha=.5, label='Right Branch')
        ax1.legend(loc="upper right")
        ax1.set_title('ID Label Difference')
        ax1.set_xlabel('Parent ID label')
        ax1.set_ylabel('CellID - ParentID')

        ax2.plot(x, y3, color='lime', alpha=.5, label='Left Branch')
        ax2.plot(x, y4, color='blueviolet', alpha=.5, label='Left Branch')
        ax2.legend(loc="upper right")
        ax2.set_title('ID Label Ratio')
        ax2.set_xlabel('Parent ID label')
        ax2.set_ylabel('CellID / ParentID')

        plt.show()
        plt.close()
