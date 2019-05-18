import os

def GetMovieFilesPaths(exp_type = "MDCK_WT_Pure"):
    """ Get the absolute paths of all movies available for analysis.
        Folders to iterate: "MDCK_WT_Pure" or "MDCK_Sc_Tet-_Pure"

    Args:
        exp_type (string, "MDCK_WT_Pure" by default)    -> change to "MDCK_Sc_Tet-_Pure" if needed.

    Return:
        xml_file_list, txt_file_list  ->  Two lists of absolute paths to all available movies for analysis. """

    xml_file_list = []
    txt_file_list = []

    directory = "/Volumes/lowegrp/Data/Kristina/{}/".format(str(exp_type))
    dir_list = [item for item in os.listdir(directory) if item != ".DS_Store"]
    for folder_date in dir_list:
        directory = "/Volumes/lowegrp/Data/Kristina/{}/{}/".format(exp_type, folder_date)  # re-initialise the native string
        dir_list = [item for item in os.listdir(directory) if item != ".DS_Store"]
        for folder_pos in dir_list:
            directory = "/Volumes/lowegrp/Data/Kristina/{}/{}/{}/".format(exp_type, folder_date, folder_pos)  # re-initialise the native string
            directory_xml = directory + "tracks/tracks_type1.xml"
            xml_file_list.append(directory_xml)
            directory_txt = directory + "analysis/cellIDdetails_raw.txt"
            txt_file_list.append(directory_txt)

    return xml_file_list, txt_file_list
