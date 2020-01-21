# Design the function to delete a specific directory (=folder) with all its contents:

import os
import shutil

def DeleteFolderWithContents(directory):
    shutil.rmtree(path=directory, ignore_errors=True)
    print ("Directory {} & all its contents have been removed.".format(directory))


def DeleteFile(file):
    os.remove(path=file)
    print("File {} has been removed.".format(file))


directory = "/Volumes/lowegrp/Data/Kristina/Training_Data/"
DeleteFolderWithContents(directory=directory)