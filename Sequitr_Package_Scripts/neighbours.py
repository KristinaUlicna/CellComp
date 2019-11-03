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

__author__ = "Alan R. Lowe"
__email__ = "code@arlowe.co.uk"

import os
import logging

import numpy as np
from scipy import spatial

from Sequitr_Package_Scripts import tracker



logger = logging.getLogger('worker_process')


class FrameMap(object):
    """ A class to deal with mapping tracks to frames and vice versa """
    def __init__(self):
        self.__tracks = None
        self.__framemap = {}
        self.__tracks = []

    @property
    def frames(self):
        """ Return the frames in the movie """
        return tuple(set(self.__framemap.keys()))

    @property
    def tracks(self):
        return self.__tracks

    def __len__(self):
        return len(self.frames)

    def add_tracks(self, tracks):
        """ Take a list of track objects, append them and update the frame mapping """
        self.__tracks += tracks

        logging.info('Adding tracks to frame map...')
        for t in tracks:
            for n in t.n:
                self.add_track_to_frame(t, n)

    def add_track_to_frame(self, track, frame):
        """ Add a track to the frame map """

        if not isinstance(track, tracker.Track):
            raise TypeError('Track is not of the correct type')

        if frame<0 or frame>2000:
            raise ValueError('Frame number is outside range 0-2000')

        if frame in self.__framemap:
            self.__framemap[frame].append(track)
        else:
            self.__framemap[frame] = [track]

    def get_tracks_by_frame(self, frame):
        """ get the tracks in a particular frame """
        return self.__framemap[frame]

    def get_cells_by_frame(self, frame):
        """ return the position and identity of all cells in a particular frame """
        tracks = self.get_tracks_by_frame(frame)
        cells = [t.get_copy_at_frame(frame) for t in tracks]
        return cells



class Neighborhood(object):
    """ calculate the neighborhood of an object """
    def __init__(self, cells):
        self.__cells = cells
        self.__vor = spatial.Voronoi(self.points)
        self.__tri = spatial.Delaunay(self.points)

    @property
    def points(self):
        return np.array([(c.x,c.y) for c in self.__cells])

    @property
    def tri(self): return self.__tri

    @property
    def vor(self): return self.__vor

    def get_voronoi_cell_by_ID(self, ID):
        """ get the points for the voronoi cell by centre cell ID """
        v_i = self.vor.point_region[ID]
        v_r = self.vor.regions[v_i]
        v_p = self.vor.vertices[v_r,:]
        v_p = np.vstack((v_p, v_p[0,:]))
        return v_p

    def get_neighbors_by_ID(self, ID, d_thresh=100.):
        """ get the IDs of the topological neighboring cells by ID """

        # set up the output structure
        output =  {'n_total': None,
                   'n_winner': None,
                   'n_loser': None,
                   'refs': [],
                   'removed': []}

        # get the simplices of the neighboring cells
        simplices = [i for i,s in enumerate(self.tri.simplices) if ID in s]

        # now make a set of the cell ID
        neighbors = set()
        for s in simplices:
            neighbors.update(self.tri.simplices[s].tolist())


        if not neighbors:
            print (ID, neighbors, simplices)
            return output


        # remove the target ID
        neighbors.remove(ID)
        neighbors = list(neighbors)

        # now prune the list of neighbors by distance
        to_remove = []
        for n in neighbors:
            dx = self.__cells[ID].x - self.__cells[n].x
            dy = self.__cells[ID].y - self.__cells[n].y
            d = np.sqrt((dx**2)+(dy**2))
            if d > d_thresh:
                to_remove.append((n, d))

        for r,d in to_remove:
            neighbors.remove(r)

        n_winner = sum([self.__cells[n].cell_type  is "winner" for n in neighbors])
        n_loser = sum([self.__cells[n].cell_type is "loser" for n in neighbors])

        output['n_total'] = n_total = len(neighbors)
        output['n_winner'] = n_winner
        output['n_loser'] = n_loser
        output['refs'] = [self.__cells[n].ref for n in neighbors]
        output['removed'] = to_remove

        return output

    def local_density_by_ID(self, ID):
        """ calculate the local density """
        # n = self.get_neighbors_by_ID(ID)
        # get the simplices of the neighboring cells
        simplices = [s for i,s in enumerate(self.tri.simplices) if ID in s]

        # now make a set of the cell ID
        density = [1./self.__area_simplex(s) for s in simplices]
        return {'local_density': sum(density)}


    def __area_simplex(self, simplex):
        """ Return the area of a simplex based on Heron's formula
        https://en.wikipedia.org/wiki/Heron%27s_formula
        """

        A = lambda a,b,c: 0.25*np.sqrt( ((a**2)+(b**2)+(c**2))**2 -
                                        2.*((a**4)+(b**4)+(c**4)) )

        euclidean_dist = lambda p0, p1: np.sqrt(np.sum((p1-p0)**2))

        pts = np.vstack([self.tri.points[s] for s in simplex])
        a = euclidean_dist(pts[0,:], pts[1,:])
        b = euclidean_dist(pts[1,:], pts[2,:])
        c = euclidean_dist(pts[2,:], pts[0,:])
        return A(a,b,c)+1e-300








def check_whether_neighborhood_exists(winner_fn):
    winner_fn, ext = os.path.splitext(winner_fn)
    winner_fn = winner_fn+"_nhood.xml"
    return os.path.exists(winner_fn)







def calculate_neighborhood(winner_fn=None,
                           loser_fn=None,
                           d_thresh=100.):
    """ Calculate the neighborhood of all cells based on the Delaunay triangulation
    returning the number and type of cells as well as a measure of local density. """

    if check_whether_neighborhood_exists(winner_fn):
        print ("{} Skipping...".format(winner_fn))
        return

    # load the XML files
    winner_xml = tracker.read_XML(winner_fn, cell_type="winner")
    loser_xml = tracker.read_XML(loser_fn, cell_type="loser")

    # set up the frame map object
    frame_map = FrameMap()
    frame_map.add_tracks(winner_xml)
    frame_map.add_tracks(loser_xml)


    # iterate over the frames, grab the cells found in each frame and calculate the neighborhood

    for f in frame_map.frames:

        # give the user some updates
        if f % 100 == 0:
            print ("Completed {} of {} frames...".format(f, len(frame_map)))

        # get all of the cell observations in a particular frame
        cells = frame_map.get_cells_by_frame(f)

        if len(cells) < 3:
            print ("Not enough cells in frame {}... skipping".format(f))
            dummy =  {'n_total': None,
                      'n_winner': None,
                      'n_loser': None,
                      'refs': [],
                      'removed': [],
                      'local_density': float('inf'),
                      'frame': f}
            for c in cells:
                c.ref.neighborhood.append(dummy)

            continue


        # now calculate the neighborhood
        N = Neighborhood(cells)


        # iterate over the cells and calculate the properties
        for i, c in enumerate(cells):

            neighbors = N.get_neighbors_by_ID(i, d_thresh=d_thresh)
            local_density = N.local_density_by_ID(i)

            neighborhood = neighbors
            neighborhood['local_density'] = local_density['local_density']
            neighborhood['frame'] = f

            # print f, c.ID, neighborhood

            # update the original Track object to contain the new info
            c.ref.neighborhood.append(neighborhood)



    winner_tracks = [t for t in frame_map.tracks if t.cell_type is "winner"]
    loser_tracks = [t for t in frame_map.tracks if t.cell_type is "loser"]

    # make new augmented filenames
    winner_fn, ext = os.path.splitext(winner_fn)
    loser_fn, ext = os.path.splitext(loser_fn)

    winner_fn = winner_fn+"_nhood.xml"
    loser_fn = loser_fn+"_nhood.xml"

    tracker.write_XML(winner_fn, winner_tracks)
    tracker.write_XML(loser_fn, loser_tracks)



# Call the function 'calculate_neighborhood':
wnr = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/tracks_try_51/tracks/tracks_type1.xml"
lsr = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/tracks_try_51/tracks/tracks_type2.xml"
calculate_neighborhood(winner_fn=wnr, loser_fn=lsr, d_thresh=100.0)