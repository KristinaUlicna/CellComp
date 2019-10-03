#Parsing XML files (from 'https://docs.python.org/2/library/xml.etree.elementtree.html'):

#XML = 'Extensible Markup Language'

    #Reading the file from disk:
import xml.etree.ElementTree as ET
tree = ET.parse('/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml')
root = tree.getroot()

    #Reading the data as a string:
"""root = ET.fromstring('/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml')"""

    #As an 'Element', root has a tag and a dictionary of attributes:
print ("Root Tag: {}".format(root.tag))
print ("Root Attributes: {}".format(root.attrib))

    #Root 'element' has children nodes over which we can iterate:
cell_counter = 0
for child in root:
    cell_counter += 1
    if cell_counter == 1:
        print ("Child Tag: {}".format(child.tag), "Child Attributes: {}".format(child.attrib))
print ("Total Cell #: {}".format(cell_counter))

    #Children are nested, and we can access specific child nodes by index:
print ("\nHERE!")
print (root)
print (root.tag)
print (root.attrib)
print (root.text)

print (root[0])             #trajectory: has a tag & dictionary of attributes, but no text
print (root[0].tag)
print (root[0].attrib)          #cell id = 88
print (root[0].text)

print (root[0][0])          #length
print (root[0][0].text)
print (root[0][1])          #fate
print (root[0][1].text)
print (root[0][2])          #x
print (root[0][2].text)
print (root[0][3])          #y
print (root[0][3].text)
print (root[0][4])          #n
print (root[0][4].text)
print (root[0][5])          #class
print (root[0][5].text)
print (root[0][6])          #parent
print (root[0][6].text)
"""print (root[0][7])"""          #none => there are only 7 layers! 'Process finished with exit code 1'
"""print (root[0][7].text)"""


    #Finding interesting elements - functions to use:
"""
Element.iter()
Element.findall()
Element.find()
Element.get()
Element.text()
"""

    #Element has some useful methods that help iterate recursively over all the sub-tree below it (its children,
    #their children, and so on). For example, Element.iter():

print ("ELEMENT.ITER()")
for parent in root.iter('parent'):      #data structure = <parent>None</parent> ... 'None' is .text, not attribute
    print (parent.text)

for trajectory in root.findall('trajectory'):
    parent = trajectory.find('parent').text
    cellID = trajectory.get('id')
    print ("Cell ID: {}, parent {}".format(cellID, parent))