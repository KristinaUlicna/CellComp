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

# You need to be connected to the server!
# Server directory absolute path: "/Volumes/lowegrp/JobServer/jobs/"
print ("Does server path exist? {}".format(os.path.exists("/Volumes/lowegrp/JobServer/jobs/")))

"""
        Text of the SEGMENTATION & CLASSIFICATION job text file:
[job]
complete = False
id = f2dafed81fd87a66bf0028a16b1473cd
user = Kristina
priority = 99
time = (2019-04-23)_15-20-00
module = jobs
func = SERVER_segment_and_classify
device = GPU
params = {'path': '/mnt/lowe-sn00/Data/Kristina/MDCK_WT_Pure/17_07_24/pos6/',
'image_dict':{'brightfield':'BF_pos6.tif','gfp':'GFP_pos6.tif',
'rfp':'RFP_pos6_noise.tif'}, 'shape':(1200,1600)}


        Text of the TRACKING job text file:
[job]
complete = False
id = Data_2
user = Kristina
priority = 99
time = (2019-05-09)_11-35-00
lib_path = /home/alan/code/BayesianTracker/
module = bworker
func = SERVER_track
device = CPU
params = {'path': '/mnt/lowe-sn00/Data/Kristina/MDCK_WT_Pure/17_07_31/pos8/', 'volume':((0,1200),(0,1600),(-1,1),(0,1200)), 'to_track':['GFP'], 'config': 'MDCK_config_Kristina.json'}
options = {}
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


    def SegClass(self, BF=True, GFP=True, RFP=False):
        """ Segmentation & Classification of the BF, GFP & RFP movies.

        Args (Boolean; 'False' if only the 'noise' movie is provided):
            Uses 3 .tif files (brightfield, GFP, RFP, which should be stored in the posX folder.
            Supply the noise movies as Channel_posX_noise.tif (e.g. RFP_pos6_noise.tif).
            I'm only mapping pure populations, so 'RFP=False' or 'RFP_posX_noise.tif' set as default.

        Return (overall output):
            An HDF file ('segmented.hdf5') saved in the folder from which movies were supplied. """

        # Create a .job file:
        job_name = 'JOB_SegClass_{}_{}_{}_pos{}'.format(self.today_date, self.user, self.data_date, self.pos)
        self.job_file = open('/Volumes/lowegrp/JobServer/jobs/' + job_name + '.job', 'w')

        # Define what goes into the file:
        movie = [BF, GFP, RFP]
        channels = ['BF', 'GFP', 'RFP']
        for order, item in enumerate(movie):
            if item:
                channels[order] += '_pos' + str(self.pos) + '.tif'
            else:
                channels[order] += '_pos' + str(self.pos) + '_noise.tif'

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/'\
            .format(str(self.user), str(self.exp_type), str(self.data_date), str(self.pos))

        string = '[job]\ncomplete = False\nid = f2dafed81fd87a66bf0028a16b1473cd\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nmodule = jobs\n'
        string += 'func = SERVER_segment_and_classify\ndevice = GPU\n'
        string += 'params = {"path": "' + str(path) + '", "image_dict": {"brightfield": "' + channels[0] + '", ' \
                        '"gfp": "' + channels[1] + '", "rfp": "' + channels[2] + '"}, "shape": (1200, 1600)}\n'

        #print (string)
        self.job_file.write(string)
        self.job_file.close()


    def Tracking(self, to_track_GFP=True, to_track_RFP=False):
        """ Tracking of the GFP & RFP movies against the brightfield.

        Args (Boolean; 'True' if channel is to be tracked, 'False' if omitted, i.e for pure populations):
            Default settings: 'to_track_GFP=True, to_track_RFP=False'
            Uses an HDF file ('segmented.hdf5') saved in the folder from which movies were supplied as SegClass input.

        Return:
            Creates 4 files: 'hypothesis_typeX.txt', 'optimised_typeX.txt', 'tracks_typeX.mat', 'tracks_typeX.xml'.
            (X = 1 for 'GFP', X = 2 for 'RFP')
            All saved inside the HDF folder with 'segmented.hdf5' file which was used as input for tracking.
            TODO: Check if formatted parameters work well!
        """

        # Did the SegClass job ran as expected? Check for HDF folder and/or 'segmented.hdf5' file:
        if os.path.isdir('/Volumes/lowegrp/Data/{}/{}/{}/pos{}/HDF' \
                                 .format(self.user, self.exp_type, self.data_date, self.pos)) is False \
            or os.path.exists('/Volumes/lowegrp/Data/{}/{}/{}/pos{}/HDF/segmented.hdf5' \
                                 .format(self.user, self.exp_type, self.data_date, self.pos)) is False :
            raise Exception("Warning: No 'HDF' folder or 'segmented.hdf5' file supplied", \
                            "Run the 'SegClass' function first")

        # Create a .job file:
        job_name = 'JOB_Tracking_{}_{}_{}_pos{}'.format(self.today_date, self.user, self.data_date, self.pos)
        #self.job_file = open('/Volumes/lowegrp/Data/{}/{}/'.format(self.user, self.type) + job_name + '.job', 'w')
        self.job_file = open('/Volumes/lowegrp/JobServer/jobs/' + job_name + '.job', 'w')

        # Define what goes into the file:
        tracks = [to_track_GFP, to_track_RFP]
        channels = ["GFP", "RFP"]
        for order, item in enumerate(tracks):
            if item is False:
                del channels[order]

        frame_volume = 1200
        if self.exp_type == "MDCK_Sc_Tet-_Pure" or self.exp_type == "MDCK_Sc_Tet+_Pure":
            frame_volume = 1400

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/' \
                .format(str(self.user), str(self.exp_type), str(self.data_date), str(self.pos))

        string = '[job]\ncomplete = False\nid = Data_2\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nlib_path = /home/alan/code/BayesianTracker/\n'
        string += 'module = bworker\nfunc = SERVER_track\ndevice = CPU\n'
        string += 'params = {"path": "{}", "volume":((0,1200),(0,1600),(-1,1),(0,{})), '.format(path, frame_volume)
        string += '"to_track":{}, "config": "MDCK_config_Kristina_relax.json"}\n'.format(channels)
        string += 'options = {}'

        print (string)
        self.job_file.write(string)
        self.job_file.close()