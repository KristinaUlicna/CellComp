import os

def GetMovieFilesPaths(exp_type = "MDCK_WT_Pure"):
    """ Get the absolute paths of all movies available for analysis.
        Folders to iterate: "MDCK_WT_Pure" or "MDCK_Sc_Tet-_Pure"

    Args:
        exp_type (string, "MDCK_WT_Pure" by default)    -> change if needed.
                  - options: "MDCK_Sc_Tet-_Pure", "MDCK_Sc_Tet+_Pure", "MDCK_90WT_10Sc_NoComp"

    Return:
        xml_file_list, txt_file_list  ->  Two lists of absolute paths to all available movies for analysis.

    Notes:
        Outputs 'cellIDdetails_raw.txt' files, so use txt_file.replace("raw", "sorted" or "filtered") to switch.
        TODO: Make sure that "MDCK_90WT_10Sc_NoComp" will output paths for both 'GFP' and 'RFP' channels.
    """

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

            # TODO: Check with Alan if 'tracks_type1.xml' or 'tracks_type2.xml' for RFP!
            """
            if exp_type.startswith("MDCK_Sc_Tet") and exp_type.endswith("_Pure"):
                directory_xml = directory + "tracks/tracks_type2.xml"
                xml_file_list.append(directory_xml)
                directory_txt = directory + "analysis/cellIDdetails_raw.txt"
                txt_file_list.append(directory_txt)
            """

            if exp_type == "MDCK_90WT_10Sc_NoComp":
                for type in [1, 2]:
                    directory_xml = directory + "tracks/tracks_type{}.xml".format(type)
                    xml_file_list.append(directory_xml)
                for channel in ["GFP", "RFP"]:
                    directory_txt = directory + "channels/{}/analysis/cellIDdetails_raw.txt".format(channel)
                    txt_file_list.append(directory_txt)

    return xml_file_list, txt_file_list


# TODO: Check at school if this works!