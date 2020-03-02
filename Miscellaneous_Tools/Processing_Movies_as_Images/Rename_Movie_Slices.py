import os

directory = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/raw_images/"

files = os.listdir(directory)

for index, file in enumerate(sorted(files)):
    if index % 100 == 0:
        print ("Renaming file {} out of {} files".format(file, len(files)))

    if "BF" in file:
        slice = file.replace("BF_pos13", "img_channel000_position013_time00000").replace(".tif", "_z000.tif")
        #slice = file.replace("position000", "position013")
        os.rename(src=directory + file, dst=directory + slice)


# OLD: RFP_pos130000.tif
# NEW: img_channel002_position000_time000001047_z000.tif