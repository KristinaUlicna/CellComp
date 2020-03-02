import os
import re
"""
def GetMovieFilesPaths(exp_type = "MDCK_WT_Pure"):
    Get the absolute paths of all movies available for analysis.
        Folders to iterate: "MDCK_WT_Pure" or "MDCK_Sc_Tet-_Pure"

    Args:
        exp_type (string, "MDCK_WT_Pure" by default)    -> change if needed.
                  - options: "MDCK_Sc_Tet-_Pure", "MDCK_Sc_Tet+_Pure", "MDCK_90WT_10Sc_NoComp"

    Return:
        xml_file_list, txt_file_list  ->  Two lists of absolute paths to all available movies for analysis.

    Notes:
        Outputs 'cellIDdetails_raw.txt' files, so use txt_file.replace("raw", "sorted" or "filtered") to switch.

    # Initialise the lists:
    xml_file_list = []
    txt_file_list = []

    # Specify the directory:
    directory = "/Volumes/lowegrp/Data/Kristina/{}/".format(exp_type)
    dir_list = [item for item in os.listdir(directory) if item != ".DS_Store" and len(str(item)) == 8]      # len('17_07_31') == 8
    for folder_date in dir_list:
        directory = "/Volumes/lowegrp/Data/Kristina/{}/{}/".format(exp_type, folder_date)  # re-initialise the native string
        dir_list = [item for item in os.listdir(directory) if item != ".DS_Store" and "pos" in item]
        for folder_pos in dir_list:
            directory = "/Volumes/lowegrp/Data/Kristina/{}/{}/{}/".format(exp_type, folder_date, folder_pos)  # re-initialise the native string
            if exp_type == "MDCK_WT_Pure" or (exp_type.startswith("MDCK_Sc_Tet") and exp_type.endswith("_Pure")):
                directory_xml = directory + "tracks/tracks_type1.xml"
                xml_file_list.append(directory_xml)
                directory_txt = directory + "analysis/cellIDdetails_raw.txt"
                txt_file_list.append(directory_txt)

            if exp_type == "MDCK_90WT_10Sc_NoComp":
                for type in [1, 2]:
                    directory_xml = directory + "tracks/tracks_type{}.xml".format(type)
                    xml_file_list.append(directory_xml)
                for channel in ["GFP", "RFP"]:
                    directory_txt = directory + "channels/{}/analysis/cellIDdetails_raw.txt".format(channel)
                    txt_file_list.append(directory_txt)

    return xml_file_list, txt_file_list
"""


class GetMovieFilesPaths(object):

    def __init__(self, exp_type="MDCK_WT_Pure"):
        """ Exp_type Options: ["MDCK_WT_Pure" or "MDCK_Sc_Tet-_Pure" or "MDCK_90WT_10Sc_NoComp"] """

        directory = "/Volumes/lowegrp/Data/Kristina/{}".format(exp_type)

        dir_list = []
        for date in os.listdir(directory):
            if re.findall(pattern='[0-9][0-9]_[0-9][0-9]_[0-9][0-9]', string=date):
                for pos in os.listdir("{}/{}/".format(directory, date)):
                    if re.findall(pattern='^pos', string=pos):
                        dir_list.append("{}/{}/{}/".format(directory, date, pos))

        channel_list = [1, 2]
        if exp_type == "MDCK_WT_Pure":
            channel_list.pop(1)
        elif exp_type == "MDCK_Sc_Tet-_Pure":
            channel_list.pop(0)

        self.dir_list = dir_list
        self.channel_list = channel_list


    def GetTracksDirs(self):
        """ Output example: '/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos0/tracks/' """

        tracks_dir_list = [directory + "tracks/" for directory in self.dir_list]

        return tracks_dir_list


    def GetChannelXmlFiles(self, nhood=False):
        """ Output example: '/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos0/tracks/tracks_typeX.xml' """

        neighbourhood = ""
        if nhood is True:
            neighbourhood = "_nhood"

        xml_file_list = []
        for directory in self.dir_list:
            for channel in self.channel_list:
                xml_file_list.append(directory + "tracks/tracks_type{}{}.xml".format(channel, neighbourhood))

        return xml_file_list


    def GetChannelTxtFiles(self, file_type="raw"):
        """ Output example: '/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos0/
                             /analysis/channel_XFP/cellIDdetails_raw.txt'
            Possibly, specify 'filtered' file type if needed.
        """

        channels = ['GFP' if item == 1 else 'RFP' if item == 2 else None for item in self.channel_list]

        txt_file_list = []
        for directory in self.dir_list:
            for channel in channels:
                txt_file_list.append(directory + "analysis/channel_{}/cellIDdetails_{}.txt".format(channel, file_type))

        return txt_file_list



def Get_MDCK_Movies_Paths():
    """

    :return:
    """

    positions_list = []
    directory = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/"
    for folder in sorted(os.listdir(directory)):
        if folder.startswith("AB") or folder.startswith("GV"):
            folder = directory + folder
            for pos in sorted(os.listdir(folder)):
                if pos.startswith("pos"):
                    position = folder + "/" + pos + "/"
                    positions_list.append(position)
    return positions_list

