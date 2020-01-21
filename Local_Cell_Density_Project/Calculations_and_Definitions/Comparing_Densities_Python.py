# TODO: Create a 'tracks_typeX_nhood.xml' parser to extract the density from the xml file:

import xml.etree.ElementTree as ET

temp_dir = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
           "tracker_performance_evaluation/tracks_try_51/tracks/"

file_GFP = temp_dir + "tracks_type1_nhood.xml"
file_RFP = temp_dir + "tracks_type2_nhood.xml"

# Read the xml file:
tree = ET.parse(file_GFP)
root = tree.getroot()
print ("Root: {}".format(root))
print ("Root Tag: {}".format(root.tag))
print ("Root Attributes: {}".format(root.attrib))
print (len(root))

print ()
print (root[0].tag)
print (root[0].attrib)
print (root[0].text)

print ("here!")
print (list(root[0].attrib.values()))

print ()
print (root[0][0].tag)
print (root[0][0].attrib)
print (root[0][0].text)
print (root[0][1].tag)
print (root[0][2].tag)
print (root[0][3].tag)
print (root[0][4].tag)
print (root[0][5].tag)
print (root[0][6].tag)
print (root[0][7].tag)
print (root[0][8].tag)
print (root[0][9].tag)
print (root[0][10].tag)
print (root[0][11].tag)
print (root[0][12].tag)


"""
length
fate
x
y
n
class
parent
children
n_total
n_winner
n_loser
local_density
neighbors
"""

dct = {}
for cell in root:
    cell_ID = int(list(cell.attrib.values())[0])
    print (cell_ID)
    frames = int(cell[0].text)
    print (frames)

    #frames = cell[4].text.split(" ")
    #frames = [item.replace(",", "") for item in frames]
    #print ("here!", type(frames))
    #print (frames)
    frm_st = int(frames[0].replace("[", ""))
    frm_en = int(frames[-1].replace("]", ""))
    dens = cell[11].text
    print (cell_ID)
    print (frm_st)
    print (frm_en)
    print (dens)
    break
    if cell_ID not in dct:
        dct[cell_ID] = []
    dct[cell_ID].append([frame, dens])

#print (dct)