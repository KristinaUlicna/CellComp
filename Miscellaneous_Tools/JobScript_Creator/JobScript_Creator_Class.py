# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
# ----- Job Script Creator for SegClass & Tracking Jobs ----- #
#                                                             #
# ----- Creator :           Kristina ULICNA             ----- #
#                                                             #
# ----- Last updated :      13th May 2019               ----- #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# ----- Class 'ProcessMovies' with 2 functions 'SegClass' & 'Tracking'
# to write JOB notepads files & submit them to the server automatically:

import os
import datetime
from Movie_Analysis_Pipeline.Single_Movie_Processing.Movie_Frame_Length import FindMovieLength

# You need to be connected to the server!
# Server directory absolute path: "/Volumes/lowegrp/JobServer/jobs/"
print ("Does server path exist? {}".format(os.path.exists("/Volumes/lowegrp/JobServer/jobs/")))


"""
        Text of the Alan's template TRACKING job text file: ()
[job]
complete = False
id = 96b13ff2bc772a080b20d7a20f62b449
user = Alan
priority = 99
time = (2019-08-30)_10-02-51
module = bworker
lib_path = /home/alan/code/BayesianTracker/
func = SERVER_track
device = CPU
params = {'volume': ((0, 1200), (0, 1600), (-100000.0, 100000.0), (0, 2000)), 'path': '/mnt/lowe-sn00/Data/Alan/Anna_to_process/2017_04_24/pos4', 'config': {'GFP': 'MDCK_config_wildtype.json', 'RFP': 'MDCK_config_scribble_sparse.json'}}

"""


class ProcessMovies():
    def __init__(self, xml_file=None, pos=8, data_date='17_07_31', exp_type='MDCK_WT_Pure', user='Kristina'):
        """ Class comprised of 2 functions (SegClass & Tracking) to process time-lapse movies.

        TODO: Create arg 'exp_type' with options: "MDCK_WT_Pure", "MDCK_Sc_Tet-_Pure", "MDCK_Sc_Tet+_Pure"
              Depending on this arg, the server will iterate all movies in the directory.
              Also, it will change the volume in the Tracking function => 1200 frames for 'WT', 1400 frames for 'Sc'

        Directory structure (path): "/mnt/lowe-sn00/Data/user/type/date/pos/"
        Directory from my Mac: "/Volumes/lowegrp/JobServer/jobs/" (when logged in to the server)

        Args:
            xml_file (string)   ->    This is an absolute directory to the xml_file that will be eventually created;
                                      It is only used to extract the absolute path where the source movies are saved.
            pos = position for which you have a brightfield, GFP and/or RFP movie available.
            date = date of the experiment, as stated in Anna's data folder. Set by default to '17_07_31'.
            type = name of your experiment (the subfolder/s for better organisation). Set by default to 'MDCK_WT_Pure'.
            user = your first name (capitalised first letter). Set by default to 'Kristina'.

        Return:
            None.
            Creates a .job file (.txt) and directly submits it onto JobServer to run.

        Notes:
            Run the segmentation, i.e. ProcessMovies.SegClass() first.
            Tracking will not work (raises Exception) if you provide no HDF folder to start with.

        """

        if xml_file is not None:
            xml_file_name = str(xml_file)
            xml_file_name = xml_file_name.split("/")
            self.pos = xml_file_name[-3].split('pos')[-1]
            self.data_date = xml_file_name[-4]
            self.exp_type = xml_file_name[-5]
            self.user = xml_file_name[-6]
        else:
            self.pos = pos
            self.data_date = data_date
            self.exp_type = exp_type
            self.user = user

        now = datetime.datetime.now()
        time = [str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute), str(now.second)]
        time = ['0' + item if len(item) < 2 else item for item in time]
        self.current_time = "({}-{}-{})_{}-{}-{}".format(time[0], time[1], time[2], time[3], time[4], time[5])
        self.today_date = str(self.current_time.split('_')[0].split('(')[1].split(')')[0])
        self.jobs_dir = '/mnt/lowe-sn00/lowegrp/JobServer/jobs/'


    def SegClass(self, BF=False, GFP=False, RFP=False, ResNet=False):
        """ Segmentation & Classification of the BF, GFP & RFP movies.

        Args (Boolean; 'False' if only the 'noise' movie is provided):
            Uses 3 .tif files (brightfield, GFP, RFP, which should be stored in the posX folder.
            Supply the noise movies as Channel_posX_noise.tif (e.g. RFP_pos6_noise.tif).
            I'm only mapping pure populations, so 'RFP=False' or 'RFP_posX_noise.tif' set as default.

        Return (overall output):
            An HDF file ('segmented.hdf5') saved in the folder from which movies were supplied.

        TODO:
            SERVER_segment_classify_and_track - ask Alan for JobScript specification & create class function.
        """

        # Define which UNet to use; classic or residual:
        network = 'U'
        if ResNet is True:
            network = 'Res' + network

        # Create a .job file:
        job_name = 'JOB_SegClass_{}_{}_{}_pos{}_{}net' \
                        .format(self.today_date, self.user, self.data_date, self.pos, network)
        self.job_file = open('/Volumes/lowegrp/JobServer/jobs/' + job_name + '.job', 'w')

        # Define what goes into the file:
        movie = [BF, GFP, RFP]
        channels = ['BF', 'GFP', 'RFP']
        for order, item in enumerate(movie):
            if item:
                channels[order] += '_pos' + str(self.pos) + '.tif'
            else:
                channels[order] = 'GAUSSIAN_NOISE'

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/' \
            .format(str(self.user), str(self.exp_type), str(self.data_date), str(self.pos))

        string = '[job]\ncomplete = False\nid = Kristina_Segment_and_Classif\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nmodule = jobs\n'
        string += 'func = SERVER_segment_and_classify\ndevice = GPU\ntimeout = 3600\n'
        string += 'params = {"path": "' + str(path) + '", "image_dict": {"brightfield": "' + channels[0] + '", ' \
                    '"gfp": "' + channels[1] + '", "rfp": "' + channels[2] + '"}, "shape": (1200, 1600), "model": "' \
                    + str(network) + 'Net2D_competition", "unet_type": "' + str(network) + 'Net2D"}\n'

        #print (string)
        self.job_file.write(string)
        self.job_file.close()

        return string

        # TODO: When segmenting Guilia's movies from posX_aligned folders, just say '' as image_dict inputs.


    def Tracking(self, to_track_GFP=False, to_track_RFP=False, timeout_seconds=7200, config_number=""):
        """ Tracking of the GFP & RFP movies against the brightfield.

        Args (Boolean; 'True' if channel is to be tracked, 'False' if omitted, i.e for pure populations):
            Default settings: 'to_track_GFP=True, to_track_RFP=False'
            Uses an HDF file ('segmented.hdf5') saved in the folder from which movies were supplied as SegClass input.
            timeout_seconds     (int)
            config_number       (int, empty str by default)

        Return:
            Creates 4 files: 'hypothesis_typeX.txt', 'optimised_typeX.txt', 'tracks_typeX.mat', 'tracks_typeX.xml'.
            (X = 1 for 'GFP', X = 2 for 'RFP')
            All saved inside the HDF folder with 'segmented.hdf5' file which was used as input for tracking.
        """

        # Did the SegClass job ran as expected? Check for HDF folder and/or 'segmented.hdf5' file:
        hdf_dir = '/Volumes/lowegrp/Data/{}/{}/{}/pos{}/HDF'.format(self.user, self.exp_type, self.data_date, self.pos)
        if config_number != "":
            #hdf_dir = '/Volumes/lowegrp/Data/{}/{}/{}/pos{}/tracker_performance_evaluation/tracks_try_{}/HDF'\
            #            .format(self.user, self.exp_type, self.data_date, self.pos, config_number)
            hdf_dir = '/Volumes/lowegrp/Data/{}/{}/{}/pos{}/HDF' \
                .format(self.user, self.exp_type, self.data_date, self.pos)

        if os.path.isdir(hdf_dir) is False or os.path.exists(hdf_dir + '/segmented.hdf5') is False:
            raise Exception("Warning: No 'HDF' folder or 'segmented.hdf5' file supplied in the specified directory!")

        # Create a .job file:
        job_name = 'JOB_Tracking_{}_{}_{}_pos{}'.format(self.today_date, self.user, self.data_date, self.pos)
        if config_number != "":
            job_name += "_Config_{}".format(config_number)
        #self.job_file = open('/Volumes/lowegrp/Data/{}/{}/'.format(self.user, self.exp_type) + job_name + '.job', 'w')
        self.job_file = open('/Volumes/lowegrp/JobServer/jobs/' + job_name + '.job', 'w')

        # Define what goes into the file:
        tracks = [to_track_GFP, to_track_RFP]
        channels = ["GFP", "RFP"]
        for order, item in enumerate(tracks):
            if item is False:
                del channels[order]

        frame_volume = FindMovieLength(exp_type=self.exp_type, data_date=self.data_date, pos="pos" + str(self.pos))
        frame_volume += 1

        """
        #if self.exp_type == "MDCK_WT_Pure":
        #    frame_volume = 1200
        if self.exp_type == "MDCK_90WT_10Sc_NoComp":
            if self.data_date == "17_03_27":
                frame_volume = 1447
            if self.data_date == "17_07_24":
                frame_volume = 1105
        """

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/' \
                .format(self.user, self.exp_type, self.data_date, self.pos)
        config = '"MDCK_config_wildtype.json"'

        if config_number != "":
            path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/tracker_performance_evaluation/tracks_try_{}/' \
                .format(self.user, self.exp_type, self.data_date, self.pos, config_number)
            config = "'MDCK_config_Kristina_Try_{}.json'".format(config_number)

        string = '[job]\ncomplete = False\nid = Kristina_Re_Tracking\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nlib_path = /home/alan/code/BayesianTracker/\n'
        string += 'module = bworker\nfunc = SERVER_track\ndevice = CPU\ntimeout = ' + str(timeout_seconds) + '\n'
        string += 'params = {"path": "' + str(path) + '", "volume":((0,1200),(0,1600),(-100000.0, 100000.0),(0,' \
                    + str(frame_volume) + ')), "config": {"GFP": ' + str(config) + ', "RFP": ' + str(config) + '}}'

        #print (string)
        self.job_file.write(string)
        self.job_file.close()

        return string