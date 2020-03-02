import os
import json
import h5py


class Process_LBEPR_Table(object):

    def __init__(self, hdf5_file, channel="GFP"):
        """ Process the tracking information stored in the LBEPR table.

        :param hdf5_file: (str)     -> absolute directory to the 'segmented.hdf5' file
        :param channel: (str)       -> "GFP" or "RFP" which will translate into obj_type_{} '1' or '2', respectively
        """

        self.ch = [1 if [channel][0] == "GFP" else 2 for _ in [channel]][0]
        self.channel = channel
        self.hdf5_file = hdf5_file
        self.lbepr = list(h5py.File(hdf5_file, 'r')["tracks"]["obj_type_{}".format(self.ch)]["LBEPR"])


    def ShortlistNonRootNonLeafCells(self, print_stats=False, use_json_files=False):
        """ Return a list of cells for which you know the entire cell cycle duration (i.e. are non-root & non-leaf).
            Use the HDF5 file (default) or cross-check with the JSON files if unsure. Value error raised in discrepancy.
        """

        # Use the initiated LBEPR table from HDF5 file (default) to extract 'true cells':
        cells = []
        for cell_info in self.lbepr:
            if int(cell_info[3]) != int(cell_info[4]):
                cells.append(int(cell_info[3]))
        cells = sorted(list(set(cells)))

        # Cross-check the correctness of the LBEPR table using the individual JSON files:
        if use_json_files is True:
            tracks = []
            tracks_directory = self.hdf5_file.replace("HDF/segmented.hdf5", "tracks/tracks_{}/".format(self.channel))
            tracks_dir = sorted(os.listdir(tracks_directory))
            for track in tracks_dir:
                file = tracks_directory + track
                id = int(track.split("track_")[-1].split("_{}.json".format(self.channel))[0])

                if id % 100 == 0:
                    print("Processing track #{}".format(id))

                with open(file, 'r') as json_file:
                    data = json.load(json_file)
                    if int(data['parent']) != 0 and data['children'] != []:
                        tracks.append(id)
            tracks = sorted(list(set(tracks)))

        if print_stats is True:
            print ("HFD5 File: {}% of true cells: {} out of total cells: {} is non-root & non-leaf.\n{}"
                   .format(round(100*len(cells)/len(self.lbepr), 2), len(cells), len(self.lbepr), cells))
            if use_json_files is True:
                print ("JSON File: {}% of true cells: {} out of total cells: {} is non-root & non-leaf.\n{}"
                      .format(round(100 * len(tracks) / len(tracks_dir), 2), len(tracks), len(tracks_dir), tracks))
                if cells == tracks:
                    print ("Lists are matching.")
                else:
                    raise ValueError("Lists are not matching.")

        return cells


    def FindBothChildrenOfParent(self):
        """ """

        children = []
        for cell_info in self.lbepr:
            mini_list = []
            for cells in self.lbepr:
                if int(cell_info[0]) == int(cells[3]):
                    mini_list.append(int(cells[0]))
            if not mini_list:
                mini_list = [0, 0]
            if len(mini_list) != 2:
                raise ValueError("Cell {} was identified to has incorrect number of children."
                                 .format(int(cell_info[0]), len(mini_list)))
            children.append(sorted(mini_list))

        return children


    def FindGenerationalDepth(self):
        """ """

        def TraverseGenerations(cell_id, accumm_generation):
            for cell_info in self.lbepr:
                parent = int(cell_info[3])
                if int(cell_info[0]) == cell_id:
                    if parent == 0:
                        return accumm_generation
                    elif parent == int(cell_info[4]):
                        return accumm_generation + 1
                    else:
                        return TraverseGenerations(cell_id=parent, accumm_generation=accumm_generation + 1)

        generation = []
        for cell_info in self.lbepr:
            gen = TraverseGenerations(cell_id=int(cell_info[0]), accumm_generation=0)
            generation.append(gen)

        return generation


    def CalculateCellCycleDuration(self):
        """ Note: If a cell (object) only appears for 1 frame, it is calculated to live for 0 minutes.
            TODO: Is this correct? Change by '+ 0' in the equation!
        """

        duration = []
        for cell_info in self.lbepr:
            cct = round((float(cell_info[2] - cell_info[1] + 0)) * 4 / 60, 4)
            duration.append(cct)

        return duration


    def __exit__(self):
        self.hdf5_file.close()