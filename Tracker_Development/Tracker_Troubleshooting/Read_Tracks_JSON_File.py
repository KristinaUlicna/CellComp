import json
import matplotlib.pyplot as plt

def ReadTracksJSON(track_number):
    file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
           "tracks_try_50/tracks/tracks_RFP/track_{}_RFP.json".format(track_number)
    with open(file) as json_file:
        data = json.load(json_file)
        print (len(data['t']), data['t'][0], data['t'][-1])
        for counter, (point_x, point_y) in enumerate(zip(data['x'], data['y'])):
            #print(counter, point_x, point_y)
            plt.scatter(y=1200-point_x, x=point_y)
        plt.ylim(0, 1200)
        plt.xlim(0, 1600)
        plt.show()


for i in range(1, 90):
    print ("\n\tReading file tracks_{}_RFP.json".format(i))
    try:
        ReadTracksJSON(track_number=i)
    except:
        continue