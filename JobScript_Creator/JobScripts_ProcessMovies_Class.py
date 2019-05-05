#TODO: Write a function which will write the JOB notepads automatically & submits them onto the server.

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
time = (2019-04-15)_12-20-00
lib_path = /home/alan/code/BayesianTracker/
module = bworker
func = SERVER_track
device = CPU
params = {'path': '/mnt/lowe-sn00/Data/Kristina/MDCK_WT_Pure/17_07_31/pos6/', 'volume':((0,1200),(0,1600),(-1,1),(0,1200)), 'to_track':'GFP'}
options = {}
"""

# You need to be connected to the server!
# Path: '/Volumes/lowegrp/JobServer/jobs/'

class ProcessMovies():
    def __init__(self, pos, data_date='17_07_31', type='MDCK_WT_Pure', user='Kristina'):
        """Class comprised of 2 functions (SegClass & Tracking) to process time-lapse movies.

        Directory structure (path): "/mnt/lowe-sn00/Data/user/type/date/pos/"
        Directory from my Mac: "/Volumes/lowegrp/JobServer/jobs/" (when logged in to the server)

        Args:
            pos = position for which you have a brightfield, GFP and/or RFP movie available.
            date = date of the experiment, as stated in Anna's data folder. Set by default to '17_07_31'.
            type = name of your experiment (the subfolder/s for better organisation). Set by default to 'MDCK_WT_Pure'.
            user = your first name (capitalised first letter). Set by default to 'Kristina'.
        Return:
            Creates a .job file (.txt) and directly submits it onto JobServer to run.
        Note:
            Run the segmentation, i.e. ProcessMovies.SegClass() first.
            Tracking will not work (raises Exception) if you provide no HDF folder to start with.
        """

        self.pos = str(pos)         # the word 'pos' not included!
        self.data_date = data_date
        self.type = type
        self.user = user

        import datetime
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
        #self.job_file = open('/Volumes/lowegrp/Data/{}/{}/'.format(self.user, self.type) + job_name + '.job', 'w')
        self.job_file = open('/Volumes/lowegrp/JobServer/jobs/' + job_name + '.job', 'w')

        # Define what goes into the file:
        movie = [BF, GFP, RFP]
        channels = ['BF', 'GFP', 'RFP']
        for order, item in enumerate(movie):
            if item:
                channels[order] += '_pos' + self.pos + '.tif'
            else:
                channels[order] += '_pos' + self.pos + '_noise.tif'

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/'\
            .format(str(self.user), str(self.type), str(self.data_date), str(self.pos))

        string = '[job]\ncomplete = False\nid = f2dafed81fd87a66bf0028a16b1473cd\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nmodule = jobs\n'
        string += 'func = SERVER_segment_and_classify\ndevice = GPU\n'
        string += 'params = {"path": "' + str(path) + '", "image_dict": {"brightfield": "' + channels[0] + '", ' \
                        '"gfp": "' + channels[1] + '", "rfp": "' + channels[2] + '"}, "shape": (1200, 1600)}\n'

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
        """

        # Did the SegClass job ran as expected? Check for HDF folder and/or 'segmented.hdf5' file:
        import os
        if os.path.isdir('/Volumes/lowegrp/Data/{}/{}/{}/pos{}/HDF' \
                                 .format(self.user, self.type, self.data_date, self.pos)) is False \
            or os.path.exists('/Volumes/lowegrp/Data/{}/{}/{}/pos{}/HDF/segmented.hdf5' \
                                 .format(self.user, self.type, self.data_date, self.pos)) is False :
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

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/' \
                .format(str(self.user), str(self.type), str(self.data_date), str(self.pos))

        string = '[job]\ncomplete = False\nid = Data_2\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nlib_path = /home/alan/code/BayesianTracker/\n'
        string += 'module = bworker\nfunc = SERVER_track\ndevice = CPU\n'
        string += 'params = {"path": "' + str(path) + '", "volume":((0,1200),(0,1600),(-1,1),(0,1200)), ' \
                        '"to_track":' + str(channels) +'}\noptions = {}'

        self.job_file.write(string)
        self.job_file.close()