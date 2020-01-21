import os
import json
import numpy as np
import matplotlib.pyplot as plt

def VisualiseCellIDTrajectory(track_number, config_number=50):
    """ Plots the position of cell_ID in x & y coordinates on the scatter
        as would be found in the segmentation map on the particular frame.
    """

    dr = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
           "tracks_try_50/tracks/tracks_RFP/".format(config_number)

    file = dr + "track_{}_RFP.json".format(track_number)
    with open(file) as json_file:
        data = json.load(json_file)
        for x, y, t in zip(data['x'], data['y'], data['t']):
            plt.scatter(y=1200-x, x=y, label="Frame #{}".format(t))
        plt.ylim(0, 1200)
        plt.xlim(0, 1600)
        plt.xlabel("X-coordinates [pixels]")
        plt.ylabel("Y-coordinates [pixels]")
        plt.title("Trajectory of the Migration Outlier Cell_ID")
        plt.savefig(dr.replace("tracks/tracks_RFP/", "migration_outliers/")
                    + "Outlier_{}_Trajectory.png".format(track_number), bbox_inches='tight')
        plt.show()
        plt.close()


path = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
           "tracks_try_50/migration_outliers/"
outliers = [item for item in os.listdir(path=path) if "Boxplot" in item]
outliers = [item.split("Outlier_")[-1].split("_Boxplot.png")[0] for item in outliers]

for id in outliers:
    VisualiseCellIDTrajectory(track_number=id)