#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:     BayesianTracker
# Purpose:  A multi object tracking library, specifically used to reconstruct
#           tracks in crowded fields. Here we use a probabilistic network of
#           information to perform the trajectory linking. This method uses
#           positional and visual information for track linking.
#
# Authors:  Alan R. Lowe (arl) a.lowe@ucl.ac.uk
#
# License:  See LICENSE.md
#
# Created:  14/08/2014
#-------------------------------------------------------------------------------


__author__ = "Alan R. Lowe"
__email__ = "a.lowe@ucl.ac.uk"

import ctypes
import numpy as np

import utils
import constants

from datetime import datetime
from collections import OrderedDict
import itertools




class PyTrackObject(ctypes.Structure):
    """ TrackObject

    Primitive class to store information about an object. Essentially a single
    object in a field of view, with some member variables to keep track of data
    associated with an object.

    Args:
        position: 2D/3D position
        dummy: is this a real object or a dummy object (e.g. when lost)
        label: object classification
        attributes: object attributes, essentially metadata about object

    Properties:
        probability: class label probabilities

    Notes:
        Similar to the impy TrackObject class.

        TODO(arl): Add attributes and to/from JSON functions

    """

    _fields_ = [('ID', ctypes.c_uint),
                ('x', ctypes.c_double),
                ('y', ctypes.c_double),
                ('z', ctypes.c_double),
                ('t', ctypes.c_uint),
                ('dummy', ctypes.c_bool),
                ('states', ctypes.c_uint),
                ('label', ctypes.c_int),
                ('prob', ctypes.POINTER(ctypes.c_double))]

    def __init__(self):
        self.__raw_probability = None

    @property
    def probability(self):
        return self.__raw_probability
    @probability.setter
    def probability(self, probability):
        if not isinstance(probability, np.ndarray):
            raise TypeError('.probability should be a numpy array')
        self.__raw_probability = probability
        self.prob = probability.ctypes.data_as(ctypes.POINTER(ctypes.c_double))




class PyTrackingInfo(ctypes.Structure):
    """ PyTrackingInfo

    Primitive class to store information about the tracking output.

    Params:
        error: error code from the tracker
        n_tracks: total number of tracks initialised during tracking
        n_active: number of active tracks
        n_conflicts: number of conflicts
        n_lost: number of lost tracks
        t_update_belief: time to update belief matrix in ms
        t_update_link: time to update links in ms
        t_total_time: total time to track objects
        p_link: typical probability of association
        p_lost: typical probability of losing track

    Notes:
        TODO(arl): should update to give more useful statistics, perhaps
        histogram of probabilities and timings.

    """

    _fields_ = [('error', ctypes.c_uint),
                ('n_tracks', ctypes.c_uint),
                ('n_active', ctypes.c_uint),
                ('n_conflicts', ctypes.c_uint),
                ('n_lost', ctypes.c_uint),
                ('t_update_belief', ctypes.c_float),
                ('t_update_link', ctypes.c_float),
                ('t_total_time', ctypes.c_float),
                ('p_link', ctypes.c_float),
                ('p_lost', ctypes.c_float),
                ('complete', ctypes.c_bool)]


    def to_dict(self):
        """ Return a dictionary of the statistics """
        # TODO(arl): make this more readable by converting seconds, milliseconds
        # and interpreting error messages?
        stats = {k:getattr(self, k) for k,typ in PyTrackingInfo._fields_}
        return stats








class MotionModel(object):
    """ MotionModel

    Kalman filter:
    'Is an algorithm which uses a series of measurements observed over time,
    containing noise (random variations) and other inaccuracies, and produces
    estimates of unknown variables that tend to be more precise than those that
    would be based on a single measurement alone.'

    Args:
        name: a name identifier
        measurements: the number of measurements of the system (typically x,y,z)
        states: the number of states of the system (typically >=measurements)
        A: State transition matrix
        B: Control matrix
        H: Observation matrix
        P: Initial covariance estimate
        Q: Estimated error in process
        R: Estimated error in measurements
        accuracy: integration limits for calculating the probabilities
        dt: time difference (always 1?)
        max_lost: number of frames without observation before marking as lost
        prob_not_assign: the default probability to not assign a track

    Members:
        reshape(): reshape matrices to the correct dimensions, will throw error
            if they are incorrectly sized.
        load(): load a motion model from a JSON file.

    Notes:
        This is just a wrapper for the data with a few convenience functions
        thrown in. Matrices must be stored Fortran style, because Eigen uses
        column major and Numpy uses row major storage.

    References:
        'A new approach to linear filtering and prediction problems.'
        Kalman RE, 1960 Journal of Basic Engineering
    """

    def __init__(self):
        self.name = 'Default'
        self.A = None
        self.H = None
        self.P = None
        self.G = None
        self.R = None
        self.measurements = None
        self.states = None
        self.dt = 1
        self.accuracy = 2.
        self.max_lost = constants.MAX_LOST
        self.prob_not_assign = constants.PROB_NOT_ASSIGN

    @property
    def Q(self):
        """ Return a Q matrix from the G matrix. """
        return self.G.transpose() * self.G

    def reshape(self):
        """ Reshapes matrices to the correct dimensions. Only need to call this
        if loading a model from a JSON file.

        Notes:
            Internally:
                Eigen::Matrix<double, m, s> H;
                Eigen::Matrix<double, s, s> Q;
                Eigen::Matrix<double, s, s> P;
                Eigen::Matrix<double, m, m> R;

        """
        s = self.states
        m = self.measurements

        # if we have defined a model, restructure matrices to the correct shapes
        # do some parsing to check that the model is specified correctly
        if s and m:
            shapes = {'A':(s,s), 'H':(m,s), 'P':(s,s), 'R':(m,m)}
            for m_name in shapes:
                try:
                    m_array = getattr(self, m_name)
                    r_matrix = np.reshape(m_array, shapes[m_name], order='C')
                except ValueError:
                    raise ValueError('Matrx {0:s} is incorrecly specified. '
                        '({1:d} entries for {2:d}x{3:d} matrix.)'.format(m_name,
                        len(m_array), shapes[m_name][0],
                        shapes[m_name][1]))

                setattr(self, m_name, r_matrix)
        else:
            raise ValueError('Cannot reshape matrices as MotionModel is '
                            'uninitialised')

    @staticmethod
    def load(filename):
        """ Load a model from file """
        return utils.read_motion_model(filename)









class ObjectModel(object):
    """ ObjectModel

    This is a class to deal with state transitions in the object, essentially
    a Hidden Markov Model.  Makes an assumption that the states are all
    observable, but with noise.

    Args:
        emission: the emission probability matrix
        transition: transition probabilities
        start: initial probabilities

    """
    def __init__(self):
        self.emission = None
        self.transition = None
        self.start = None
        self.states = None

    def reshape(self):
        """ Reshapes matrices to the correct dimensions. Only need to call this
        if loading a model from a JSON file.

        Notes:
            Internally:
                Eigen::Matrix<double, s, s> emission;
                Eigen::Matrix<double, s, s> transition;
                Eigen::Matrix<double, s, 1> start;
        """
        if not self.states:
            raise ValueError('Cannot reshape matrices as ObjectModel is '
                            'uninitialised')
        s = self.states
        self.emission = np.reshape(self.emission, (s,s), order='C')
        self.transition = np.reshape(self.transition, (s,s), order='C')

    @staticmethod
    def load(filename):
        """ Load a model from file """
        return utils.read_object_model(filename)














class Tracklet(object):
    """ Tracklet

    Tracklet object for storing and updating linked lists of track objects.
    Forms the data structure for an individual tracklet.

    Track 'fates' are the selected hypotheses after optimization:

        #define TYPE_Pfalse 0
        #define TYPE_Pinit 1
        #define TYPE_Pterm 2
        #define TYPE_Plink 3
        #define TYPE_Pdivn 4
        #define TYPE_Papop 5
        #define TYPE_Pdead 6
        #define TYPE_Pmrge 7
        #define TYPE_undef 999

    Args:
        ID: unique identifier
        data: trajectory
        kalman: Kalman filter output
        labels: class labels for each object
        fate: the fate of the track

    Members:
        __len__: length of the trajectory in frames (including interpolated)
        lost: whether the track was lost during tracking
        merge: a merging function to stitch together two tracks
        labeller: a mapping function from an integer to another label type (str)

    Properties:
        x: x position
        y: y position
        z: z position
        dummy: did this position arise from an actual measurement?
        parent:    parent tracklet
        root: root tracklet if a branching tree (ie cell division)
        motion_model: typically a reference to a Kalman filter or motion model

    Notes:
        TODO (arl) add the dummy field back, and the track merging. Also,
        clean up indexing into arrays.
    """

    def __init__(self,
                 ID,
                 data,
                 kalman=None,
                 labels=None,
                 parent=None,
                 children=[],
                 fate=None):

        self.ID = ID
        self.__data = data
        self.__kalman = kalman
        self.__labels = labels
        self.__dummy = None

        self.root = None
        self.parent = parent
        self.children = children
        self.type = None
        self.fate = fate

        # labeller is a function to convert an integer label to a string or
        # other type if required. default is to return the original integer
        self.labeller = utils.Labeller()

    def __len__(self):
        return self.__data.shape[0]

    @property
    def x(self): return self.__data[:,1].tolist()
    @property
    def y(self): return self.__data[:,2].tolist()
    @property
    def z(self): return self.__data[:,3].tolist()
    @property
    def t(self): return self.__data[:,0].tolist()
    @property
    def dummy(self): return self.__dummy

    @property
    def label(self):
        return [self.labeller(l) for l in self.__labels.tolist()]

    @property
    def fate_label(self):
        """ Return a string of the fate label """

        #TODO(arl): abstract this
        f = ['false_positive', 'initializing', 'terminating', 'link',
             'dividing', 'apoptosis', 'dead', 'merging', 'undefined']
        if self.fate is not None:
            return f[self.fate]
        else:
            return None

    def kalman(self, index):
        """ Return the entire Kalman filter output for one parameter """
        #TODO(arl): get the kalman attribute by name
        return self.__kalman[:,index]
        #raise DeprecationWarning("Use mu() and covar() instead.")

    def mu(self, index):
        """ Return the Kalman filter mu. Note that we are only returning the mu
         for the positions (e.g. 3x1) """
        return np.matrix(self.__kalman[index,1:4]).reshape(3,1)

    def covar(self, index):
        """ Return the Kalman filter covariance matrix. Note that we are
        only returning the covariance matrix for the positions (e.g. 3x3) """
        return np.matrix(self.__kalman[index,4:13]).reshape(3,3)

    def predicted(self, index):
        """ Return the motion model prediction for the given timestep. """
        return np.matrix(self.__kalman[index,13:]).reshape(3,1)

    def to_dict(self):
        """ Return a dictionary of the tracklet which can be used for JSON
        export. This is an ordered dictionary for nicer JSON output.
        """
        # TODO(arl): add the Kalman filter output here too
        trk_tuple = (('ID',self.ID), ('length',len(self)), ('root',self.root),
            ('parent',self.parent), ('x',self.x),( 'y',self.y), ('z',self.z),
            ('t',self.t),('label',self.label),('fate',self.fate))

        return OrderedDict( trk_tuple )

    def to_array(self):
        """ Return a numpy array of the tracklet which can be used for MATLAB
        export. """
        # TODO(arl): add the Kalman filter output here too
        # return np.hstack((self.__data, np.ones((len(self),1))*self.ID))
        tmp_track = np.zeros((len(trk),7), dtype='float32')
        tmp_track[:,0] = trk.x
        tmp_track[:,1] = trk.y
        tmp_track[:,2] = trk.t
        tmp_track[:,3] = trk.ID
        tmp_track[:,4] = trk.parent
        tmp_track[:,5] = trk.root
        tmp_track[:,6] = trk.label
        return tmp_track

    def in_frame(self, frame):
        """ Return true or false as to whether the track is in the frame """
        return self.__data[0,0]<=frame and self.__data[-1,0]>=frame

    def trim(self, frame, tail=75):
        """ Trim the tracklet and return one with the trimmed data """
        d = self.__data.copy()
        idx = [self.t.index(t) for t in self.t if t<=frame and t>=frame-tail]
        d = d[idx,:]
        return Tracklet(self.ID, d)


    @staticmethod
    def from_dict(track_params):
        """ Create a new tracklet using data from a dictionary """
        if not isinstance(track_params, dict):
            raise TypeError('Tracklet.from_dict requires a dictionary.')

        T = Tracklet()
        return T