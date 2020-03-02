# Design the function to delete a specific directory (=folder) with all its contents:

import os
import shutil
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths

def DeleteFolderWithContents(directory):
    shutil.rmtree(path=directory, ignore_errors=True)
    print ("Directory {} & all its contents have been removed.".format(directory))


def DeleteFile(file):
    os.remove(path=file)
    print("File {} has been removed.".format(file))


