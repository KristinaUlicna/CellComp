import os
import zipfile
from Single_Movie_Analysis.Server_Movies_Paths import GetMovieFilesPaths

xml_file_list, txt_file_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")
print (xml_file_list)

for xml_file in xml_file_list:
    zipped_file = xml_file.replace("tracks_type1.xml", "tracks_GFP.zip")
    with zipfile.ZipFile(zipped_file, "r") as zip_ref:
        extract_dir = xml_file.replace("tracks_type1.xml", "tracks_GFP/")
        if not os.path.isdir(extract_dir):
            os.makedirs(extract_dir)
        zip_ref.extractall(extract_dir)
    print ("Extraction done for {}".format(zipped_file))