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

import json

class CreateTrackerConfig(object):

    def __init__(self, try_number):

        self.try_number = try_number


    #def WriteConfigJSON(self):



# Blah blah blah...
data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}


data = {
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
            "A":
                {
                "matrix": [1,0,0,1,0,0,
                           0,1,0,0,1,0,
                           0,0,1,0,0,1,
                           0,0,0,1,0,0,
                           0,0,0,0,1,0,
                           0,0,0,0,0,1]
            },
            "H":
                {
                "matrix": [1,0,0,0,0,0,
                           0,1,0,0,0,0,
                           0,0,1,0,0,0]
            },
            "P":
                {
                "sigma": 150.0,
                "matrix": [0.1,0,0,0,0,0,
                          0,0.1,0,0,0,0,
                          0,0,0.1,0,0,0,
                           0,0,0,1,0,0,
                           0,0,0,0,1,0,
                           0,0,0,0,0,1]
            },
            "G":
                {
                "sigma": 15.0,
                "matrix": [0.5,0.5,0.5,1,1,1]

            },
            "R":
                {
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
            "hypotheses": "['P_FP', 'P_init', 'P_term', 'P_link', 'P_branch', 'P_dead']",
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
            "relax": "true"
        }
    }
}


path = "/Volumes/lowegrp/Models/BayesianTracker/json_example.json"
with open(path, 'w') as outfile:
    json.dump(data, outfile, indent=2)