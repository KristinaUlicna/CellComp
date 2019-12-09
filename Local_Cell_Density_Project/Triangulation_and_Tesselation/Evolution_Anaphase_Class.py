#TODO: Create a class which will collect the data of division distances:

import os
import json
import numpy as np
from Miscellaneous_Tools.Handy_Functions.Unzip_Zip_Files import UnzipTrackJSONfile
from Local_Cell_Density_Project.SegClass_HDF_Output_Files.HDF_Format_New.HDF5_Data_Functions import GetCellCountPerFrame


def DistanceBetweenTwoPoints(x1, y1, x2, y2):
    """ Use Pythagorean Theorem to calculate displacement of two objects with known 'x' & 'y' coordinates. """
    return np.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 )



class AnaphaseNucleiDistance(object):

    def __init__(self, txt_file):
        """ Which tracks you want to take the zipped file from."""

        zipped_file = txt_file.replace("analysis/channel", "tracks/tracks").split("/cellIDdetails")[0] + ".zip"
        directory = UnzipTrackJSONfile(zipped_file=zipped_file)
        self.hdf5_file = directory.split("/tracks/")[0] + "/HDF/segmented.hdf5"

        if os.path.isdir(directory):
            if not directory.endswith("/"):
                directory += "/"

        self.directory = directory
        self.channel = directory.split("tracks_")[-1].split("/")[0]

        self.frames_of_interest = 5
        self.parent_child = [[] for _ in range(self.frames_of_interest)]
        self.sibling_sibling = [[] for _ in range(self.frames_of_interest)]
        self.cell_count = []


    def CalculateAnaphaseDistancePerMovie(self):
        """ """

        print (self.directory)

        for file in os.listdir(self.directory):
            with open(self.directory + file) as json_file:
                data = json.load(json_file)

                if data['fate'] == "DIVIDE":
                    print ("Divides: {}".format(file))

                    x_p = float(data['x'][-1])
                    y_p = float(data['y'][-1])
                    children = [int(data['children'][0]), int(data['children'][1])]
                    frame_div = int(data['t'][-1])
                    cell_count = GetCellCountPerFrame(hdf5_file=self.hdf5_file, frame=frame_div)

                    x_c = [[] for _ in range(2)]
                    y_c = [[] for _ in range(2)]

                    for index, child in enumerate(children):
                        with open(self.directory + "track_{}_{}.json".format(child, self.channel)) as new_json_file:
                            new_data = json.load(new_json_file)

                            counter = 0
                            if int(new_data['length']) >= self.frames_of_interest:
                                while counter <= self.frames_of_interest:
                                    x_c[index].append(float(new_data['x'][counter]))
                                    y_c[index].append(float(new_data['y'][counter]))

                    if len(x_c[0]) == len(x_c[1]) == len(y_c[0]) == len(y_c[1]) == self.frames_of_interest:
                        for i in range(self.frames_of_interest):
                            for j in range(2):
                                dis_pc = DistanceBetweenTwoPoints(x1=x_p, y1=y_p, x2=x_c[j][i], y2=y_c[j][i])
                                self.parent_child[i].append(dis_pc)
                            dis_ss = DistanceBetweenTwoPoints(x1=x_c[0][i], y1=y_p[0][i], x2=x_c[1][i], y2=y_c[1][i])
                            self.sibling_sibling[i].append(dis_ss)
                        self.cell_count.append(cell_count)

        return self.cell_count, self.parent_child, self.sibling_sibling



txt_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/analysis/channel_GFP/cellIDdetails_raw.txt"
call = AnaphaseNucleiDistance(txt_file=txt_file)
cell_count, parent_child, sibling_sibling = call.CalculateAnaphaseDistancePerMovie()
print ("Cell Count = {}".format(cell_count))
print ("Parent_Child = {}".format(parent_child))
print ("Sibling_Sibling = {}".format(sibling_sibling))
