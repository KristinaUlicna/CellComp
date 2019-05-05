#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:     Sequitr
# Purpose:  Sequitr is a small, lightweight Python library for common image
#           processing tasks in optical microscopy, in particular, single-
#           molecule imaging, super-resolution or time-lapse imaging of cells.
#           Sequitr implements fully convolutional neural networks for image
#           segmentation and classification. Modelling of the PSF is also
#           supported, and the library is designed to integrate with
#           BayesianTracker.
#
# Authors:  Alan R. Lowe (arl) a.lowe@ucl.ac.uk
#
# License:  See LICENSE.md
#
# Created:  23/03/2018
#-------------------------------------------------------------------------------

__author__ = 'Alan R. Lowe'
__email__ = 'code@arlowe.co.uk'


import os
import ast
import xml.etree.cElementTree as ET





class Track(object):
    """ Dummy track object

    This has several roles. It acts as a container for information from the
    tracking code, but can also be used to calculate further features such as
    the local density of neighbors.

    Notes:
        - Future expansion

    """
    def __init__(self, ID=None):
        self.ID = ID
        self.x = None
        self.y = None
        self.z = None
        self.n = None
        self.length = None
        self.label = None
        self.parent = None
        self.children = []
        self.fate = None
        self.cell_type = None
        self.neighborhood = []

    def in_frame(self, frame):
        """ return a bool as to whether this track is present in a certain
        frame of the movie """
        return (frame in self.n)

    def __len__(self):
        return self.length

    def get_copy_at_frame(self, frame):
        """ get a copy of the object at a specific frame. This is essentially
        the cell position and state at a particular time """

        if not self.in_frame(frame): return None

        # parameters to copy versus get when duplicating a track
        to_copy = ['ID','length','parent','fate','cell_type','children']
        to_get = ['x','y','z','n','label']
        # to_get = [g for g in self.__dict__.keys() if g not in to_copy]

        # now duplicate the track, but only return the values at a certain
        # frame

        T = Track()
        T.ref = self
        for p in to_copy:
            setattr(T, p, getattr(self, p))
        for p in to_get:
            param = getattr(self, p)
            if param is None: continue
            idx = self.n.index(frame)
            setattr(T, p, param[idx])

        return T

    def get_neighborhood_attr(self, attr):
        if not isinstance(attr, str):
            raise TypeError('Attribute must be a string')
        return [n[attr] for n in self.neighborhood]


    def __getitem__(self, attr):
        """ Get an item by name! """
        if attr in self.__dict__.keys():
            return getattr(self, attr)

        if self.neighborhood:
            if attr in self.neighborhood[0].keys():
                return self.get_neighborhood_attr(attr)

        return None



def read_XML(filename, cell_type=None):
    """ Load tracks from an sequitr XML file """

    if filename is None:
        print ("Warning - no filename specified in read_XML")
        return []

    if not isinstance(filename, str):
        raise TypeError("Filename must be specified as a string")

    if not filename.endswith((".xml",".XML")):
        raise IOError("Tracking data must be in XML format")

    if not os.path.exists(filename):
        return []

    tracks = []

    XMLtree = ET.parse(filename)
    root = XMLtree.getroot()
    for track in root.findall('trajectory'):

        new_track = Track( ID = int(track.get('id')) )
        new_track.cell_type = cell_type
        for track_props in track:

            try:
                if track_props.tag == 'class':
                    new_track.label = ast.literal_eval(track_props.text)
                else:
                    setattr(new_track, track_props.tag, ast.literal_eval(track_props.text))
            except:
                print (track_props)

        tracks.append(new_track)

    return tracks






def write_XML(filename, tracks):
    """ write out the tracks to a new XML file """

    import json
    import xml.etree.cElementTree as ET

    print (filename)

    root = ET.Element("data", name=filename)

    for trk in tracks:

        if len(trk) < 1: continue

        txml = ET.SubElement(root, "trajectory", id=str(int(trk.ID)))

        ET.SubElement(txml, "length").text = str(len(trk))
        ET.SubElement(txml, "fate").text = str(trk.fate)
        ET.SubElement(txml, "x").text = str([float("{0:2.1f}".format(x)) for x in trk.x])
        ET.SubElement(txml, "y").text = str([float("{0:2.1f}".format(y)) for y in trk.y])
        ET.SubElement(txml, "n").text = str([int(t) for t in trk.n])
        ET.SubElement(txml, "class").text = str([l for l in trk.label])
        ET.SubElement(txml, "parent").text = str(trk.parent)
        ET.SubElement(txml, "children").text = str(trk.children)


        if trk.neighborhood:
            ET.SubElement(txml, "n_total").text = str([n for n in trk['n_total']])
            ET.SubElement(txml, "n_winner").text = str([n for n in trk['n_winner']])
            ET.SubElement(txml, "n_loser").text = str([n for n in trk['n_loser']])
            ET.SubElement(txml, "local_density").text = str([float("{0:2.5f}".format(d)) for d in trk['local_density']])

            ET.SubElement(txml, "neighbors").text = str([[t.ID for t in refs] for refs in trk['refs']])

    XMLtree = ET.ElementTree(root)
    XMLtree.write(filename)



if __name__ == "__main__":
    pass