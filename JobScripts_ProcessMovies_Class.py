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
params = {'path': '/mnt/lowe-sn00/Data/Kristina/MDCKwt100percent/17_07_24/pos6/',
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
params = {'path': '/mnt/lowe-sn00/Data/Kristina/MDCKwt100percent/17_07_31/pos6/', 'volume':((0,1200),(0,1600),(-1,1),(0,1200)), 'to_track':'GFP'}
options = {}
"""


class ProcessMovies:
    def __init__(self, pos, data_date='17_07_31', type='MDCKwt100percent', user='Kristina'):
        """Class comprised of 2 functions (SegClass & Track) to process time-lapse movies.

        Directory structure (path): "/mnt/lowe-sn00/Data/user/type/date/pos/"

        Args:
            pos = position for which you have a brightfield, GFP and/or RFP movie available.
            date = date of the experiment, as stated in Anna's data folder. Set by default to '17_07_31'.
            type = name of your experiment (the subfolder for better organisation). Set by default to 'MDCKwt100percent'.
            user = your first name (capitalised first letter). Set by default to 'Kristina'.
        Return:
            Creates a text file (.txt) and #TODO:directly submits a '.job' file into JobServer to run.
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


    def SegClass(self):
        """ Segmentation & Classification of the BF, GFP & RFP movies.

        Args (no input needed for this function):
            Uses 3 .tif files which should be stored in the posX folder.
            If you are only using 2 movies, supply the 3rd movie as a noise.
            (in this case, RFP_posX_noise.tif) set as default.

        Return (overall output):
            An HDF file ('segmented.hdf5') saved in the folder from which movies were supplied.

        """

        #TODO: Set a new kwarg (Boolean): noise=True
        job_name = 'JOB_SegClass_{}_{}_pos{}'.format(self.user, self.today_date, self.pos)
        self.txt_file = open('/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/' + job_name + '.txt', 'w')
        #self.job_file = open(self.jobs_dir + job_name + '.job', 'w')                  # TODO: Create a .job file too!

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/'\
            .format(str(self.user), str(self.type), str(self.data_date), str(self.pos))
        print (path)
        string = '[job]\ncomplete = False\nid = f2dafed81fd87a66bf0028a16b1473cd\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nmodule = jobs\n'
        string += 'func = SERVER_segment_and_classify\ndevice = GPU\n'
        string += 'params = {"path": "' + str(path) + '", "image_dict": {"brightfield": "BF_pos' + self.pos + '.tif", "gfp": "GFP_pos' + self.pos + '.tif", "rfp": "RFP_pos' + self.pos + '_noise.tif"}, "shape": (1200, 1600)}"\n'
        print (string)
        self.txt_file.write(string)
        self.txt_file.close()


    def Tracking(self):
        """ Tracking of the BF, GFP & RFP movies.

        Args (no input needed for this function):
            Uses an HDF file ('segmented.hdf5') saved in the folder from which movies were supplied as input.

        Return:
            Need to specify which channel to be tracked.
            Set ("to_track":["GFP"]) by default.
        """
        # TODO: Set a new kwarg (Boolean): to_track_GFP=True, to_track_RFP=False

        job_name = 'JOB_Tracking_{}_{}_pos{}'.format(self.user, self.today_date, self.pos)
        self.txt_file = open('/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/' + job_name + '.txt', 'w')
        # self.job_file = open(self.jobs_dir + job_name + '.job', 'w')                # TODO: Create a .job file too!

        path = '/mnt/lowe-sn00/Data/{}/{}/{}/pos{}/' \
            .format(str(self.user), str(self.type), str(self.data_date), str(self.pos))
        print (path)
        string = '[job]\ncomplete = False\nid = Data_2\n'
        string += 'user = ' + str(self.user) + '\npriority = 99\n'
        string += 'time = ' + str(self.current_time) + '\nlib_path = /home/alan/code/BayesianTracker/\n'
        string += 'module = bworker\nfunc = SERVER_track\ndevice = CPU\n'
        string += 'params = {"path": "' + str(path) + '", "volume":((0,1200),(0,1600),(-1,1),(0,1200)), "to_track":["GFP"]}\n'
        string += 'options = {}'
        print (string)
        self.txt_file.write(string)
        self.txt_file.close()


# Call the class & its functions:
for number in range(6, 9):
    call = ProcessMovies(number, data_date='17_07_24')
    call.SegClass()
    call.Tracking()