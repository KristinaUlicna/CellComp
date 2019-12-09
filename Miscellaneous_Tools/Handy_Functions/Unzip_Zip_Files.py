import os
import zipfile
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import GetMovieFilesPaths

def UnzipTrackJSONfile(zipped_file):
    """

    :param zipped_file:    (str)   -> absolute path to directory
    :return: None
    """

    extract_dir = zipped_file.replace(".zip", "/")

    # Simply extract all files:
    if os.path.isfile(zipped_file):
        if not os.path.isdir(extract_dir):
            os.makedirs(extract_dir)
        with zipfile.ZipFile(zipped_file, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        print ("Done for file: {}".format(zipped_file))

    return extract_dir


def UnzipTrackJSONfiles(tracks_directory, channel):
    """

    :param tracks_directory:    (str)   -> absolute path to directory
    :param channel:             (str)   -> "GFP" or "RFP"
    :return: None
    """

    # Make sure the directory ends with an '/' & the file is unzipped:
    if not tracks_directory.endswith("/"):
        tracks_directory += "/"

    zipped_file = tracks_directory + "tracks_{}.zip".format(channel)
    extract_dir = tracks_directory + "tracks_{}/".format(channel)

    # OPTION #1: There is the zipped file in the directory and it was already extracted - do nothing, but update user:
    if os.path.isfile(zipped_file) and os.path.isdir(extract_dir):
        print ("The file {} was already extracted into directory {}".format(zipped_file, extract_dir))

    # OPTION #1: There is the zipped file in the directory but it wasn't already extracted yet - extract it:
    elif os.path.isfile(zipped_file) and not os.path.isdir(extract_dir):
        with zipfile.ZipFile(zipped_file, "r") as zip_ref:
            if not os.path.isdir(extract_dir):
                os.makedirs(extract_dir)
            zip_ref.extractall(extract_dir)
        print ("The file {} was just freshly extracted into directory {}".format(zipped_file, extract_dir))

    # OPTION #3: There is no such zipped file in the directory (mainly because movie had just a single channel):
    elif not os.path.isfile(zipped_file):
        print ("There is no {} file in the specified directory {}".format(zipped_file, tracks_directory))


def UnzipTrackJSONfilesWholeExpType(exp_type):
    """

    :param exp_type: (str)  -> "MDCK_WT_Pure" or "MDCK_Sc_Tet-_Pure" or "MDCK_90WT_10Sc_NoComp"
    :return:                -> None
    """

    xml_file_list, _ = GetMovieFilesPaths(exp_type=exp_type)

    for xml_file in xml_file_list:
        tracks_directory = "/".join(xml_file.split("/")[:-1])
        channel = xml_file.split("/")[-1]
        if "tracks_type1.xml" in channel:
            channel = "GFP"
        elif "tracks_type2.xml" in channel:
            channel = "RFP"
        UnzipTrackJSONfiles(tracks_directory=tracks_directory, channel=channel)

