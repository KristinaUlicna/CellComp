""" Text of the config file:
{
  "TrackerConfig":
    {
      "MotionModel":
        {
          "name": "MDCK_motion",
          "dt": 1.0,
          "measurements": 3,
          "states": 6,
          "accuracy": 7.5,
          "prob_not_assign": 0.001,
          "max_lost": 5,
          "A": {
            "matrix": [1,0,0,1,0,0,
                       0,1,0,0,1,0,
                       0,0,1,0,0,1,
                       0,0,0,1,0,0,
                       0,0,0,0,1,0,
                       0,0,0,0,0,1]
          },
          "H": {
            "matrix": [1,0,0,0,0,0,
                       0,1,0,0,0,0,
                       0,0,1,0,0,0]
          },
          "P": {
            "sigma": 150.0,
            "matrix": [0.1,0,0,0,0,0,
                       0,0.1,0,0,0,0,
                       0,0,0.1,0,0,0,
                       0,0,0,1,0,0,
                       0,0,0,0,1,0,
                       0,0,0,0,0,1]
          },
          "G": {
            "sigma": 15.0,
            "matrix": [0.5,0.5,0.5,1,1,1]

          },
          "R": {
            "sigma": 5.0,
            "matrix": [1,0,0,
                       0,1,0,
                       0,0,1]
          }
        },
      "ObjectModel":
        {},
      "HypothesisModel":
        {
          "name": "MDCK_hypothesis_wildtype",
          "hypotheses": ["P_FP", "P_init", "P_term", "P_link", "P_branch", "P_dead"],
          "lambda_time": 5.0,
          "lambda_dist": 30.0,
          "lambda_link": 10.0,
          "lambda_branch": 50.0,
          "eta": 1e-10,
          "theta_dist": 20.0,
          "theta_time": 5.0,
          "dist_thresh": 40,
          "time_thresh": 2,
          "apop_thresh": 5,
          "segmentation_miss_rate": 0.1,
          "apoptosis_rate": 0.001,
          "relax": true
        }
    }
}

"""

#TODO: Write a function which will generate the config file:

class CreateTrackerConfig(object):

    def __init__(self, try_number):

        path = "/Volumes/lowegrp/Models/BayesianTracker/"
        file = "MDCK_config_Kristina_Try_{}.json".format(try_number)
        #file = "json_example.json"
        self.file = open(path + file, "w")
        self.try_number = try_number


    def WriteConfigFile(self,
                        prob_not_assign=0.001,
                        max_lost=5,
                        sigma_P=150.0,
                        sigma_G=15.0,
                        sigma_R=5.0,
                        lambda_time=5.0,
                        lambda_dist=30.0,
                        lambda_link=10.0,
                        lambda_branch=50.0,
                        eta=1e-10,
                        theta_dist=20.0,
                        theta_time=5.0,
                        dist_thresh=40,
                        time_thresh=2,
                        apop_thresh=5,
                        segmentation_miss_rate=0.1,
                        apoptosis_rate=0.001,
                        relax='true'):

        string = "{\n"
        string += "  'TrackerConfig':\n"
        string += "    {\n"
        string += "      'MotionModel':\n"
        string += "        {\n"
        string += "          'name': 'MDCK_motion',\n"
        string += "          'dt': 1.0,\n"
        string += "          'measurements': 3,\n"
        string += "          'states': 6,\n"
        string += "          'accuracy': 7.5,\n"
        string += "          'prob_not_assign': {},\n".format(prob_not_assign)
        string += "          'max_lost': {},\n".format(max_lost)
        string += "          'A': {\n"
        string += "            'matrix': [1,0,0,1,0,0,\n"
        string += "                       0,1,0,0,1,0,\n"
        string += "                       0,0,1,0,0,1,\n"
        string += "                       0,0,0,1,0,0,\n"
        string += "                       0,0,0,0,1,0,\n"
        string += "                       0,0,0,0,0,1]\n"
        string += "          },\n"
        string += "          'H': {\n"
        string += "            'matrix': [1,0,0,0,0,0,\n"
        string += "                       0,1,0,0,0,0,\n"
        string += "                       0,0,1,0,0,0]\n"
        string += "          },\n"
        string += "          'P': {\n"
        string += "            'sigma': {},\n".format(sigma_P)
        string += "            'matrix': [0.1,0,0,0,0,0,\n"
        string += "                       0,0.1,0,0,0,0,\n"
        string += "                       0,0,0.1,0,0,0,\n"
        string += "                       0,0,0,1,0,0,\n"
        string += "                       0,0,0,0,1,0,\n"
        string += "                       0,0,0,0,0,1]\n"
        string += "          },\n"
        string += "          'G': {\n"
        string += "            'sigma': {},\n".format(sigma_G)
        string += "            'matrix': [0.5,0.5,0.5,1,1,1]\n"
        string += "          },\n"
        string += "          'R': {\n"
        string += "            'sigma': {},\n".format(sigma_R)
        string += "            'matrix': [1,0,0,\n"
        string += "                       0,1,0,\n"
        string += "                       0,0,1]\n"
        string += "          }\n"
        string += "        },\n"
        string += "      'ObjectModel':\n"
        string += "        {},\n"
        string += "      'HypothesisModel':\n"
        string += "        {\n"
        string += "          'name': 'MDCK_hypothesis_Kristina_Try_{}',\n".format(self.try_number)
        string += "          'hypotheses': ['P_FP', 'P_init', 'P_term', 'P_link', 'P_branch', 'P_dead'],\n"
        string += "          'lambda_time': {},\n".format(lambda_time)
        string += "          'lambda_dist': {},\n".format(lambda_dist)
        string += "          'lambda_link': {},\n".format(lambda_link)
        string += "          'lambda_branch': {},\n".format(lambda_branch)
        string += "          'eta': {},\n".format(eta)
        string += "          'theta_dist': {},\n".format(theta_dist)
        string += "          'theta_time': {},\n".format(theta_time)
        string += "          'dist_thresh': {},\n".format(dist_thresh)
        string += "          'time_thresh': {},\n".format(time_thresh)
        string += "          'apop_thresh': {},\n".format(apop_thresh)
        string += "          'segmentation_miss_rate': {},\n".format(segmentation_miss_rate)
        string += "          'apoptosis_rate': {},\n".format(apoptosis_rate)
        string += "          'relax': {}\n".format(relax)
        string += "        }\n"
        string += "    }\n"
        string += "}\n"

        string = string.replace("'", '"')
        print (string)
        self.file.write(string)
        self.file.close()
