# TODO: Make a function which loops through the 'track_xxx_XFP.json' files and evaluates the tracks which may have been fused together as false divisions:

import os
import json
import zipfile

def Identify_Fake_Links(channel="RFP", config_number=52):
    """ Make a function which loops through the 'track_xxx_XFP.json' files
        and evaluates the tracks which may have been fused (=linked upon optimisation)
        together as false divisions:
        :param:
        :return:
    """

    # Extract zip file if not done so previously:
    directory = "/Volumes/lowegrp/data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
                "tracker_performance_evaluation/tracks_try_{}/tracks/tracks_{}/".format(config_number, channel)
    if not os.path.isdir(directory):
        with zipfile.ZipFile(directory[:-1] + ".zip", "r") as zip_ref:
            zip_ref.extractall(directory)

    # List directory and iterate through each json file:
    total_tracks = os.listdir(directory)
    total_counter = 0
    total_fakes_list = []

    for track_file in total_tracks:
        with open(directory + track_file) as json_file:
            data = json.load(json_file)
            length = int(data['length'])
            fake_link_label_list = [[], []]
            FOUND = False
            for order, (label, frame) in enumerate(zip(data['label'], data['t'])):
                if FOUND is False and label == 'INTERPHASE':
                    continue
                elif FOUND is False and order + 1 in list(range(1, 10)):
                    continue
                elif FOUND is False and order + 1 in list(range(length - 10, length + 1)):
                    continue
                else:
                    FOUND = True        # if something is happening:

                if FOUND is True and len(fake_link_label_list[0]) <= 10:
                    fake_link_label_list[0].append(label)
                    fake_link_label_list[1].append(frame)

        # Check whether the data pulled out are just one-off classifier mistakes (the cell goes back to 'interphase'):
        if fake_link_label_list[0]:
            counter = 0
            for item in fake_link_label_list[0]:
                if item != 'INTERPHASE':
                    counter += 1
            if counter > 7:
                #print ("Track: {}; length = {}".format(track_file, length))
                #print (fake_link_label_list[0])
                #print (fake_link_label_list[1])
                total_counter += 1
                total_fakes_list.append(track_file)

    print ("{} with possible fake-linked divisions out of {} movies in the 'tracks_{}' directory.\n"
           "List of tracks: {}".format(total_counter, len(total_tracks), channel, total_fakes_list))

    return total_fakes_list


fake_tracks_52 = Identify_Fake_Links(channel="RFP", config_number=52)
fake_tracks_53 = Identify_Fake_Links(channel="RFP", config_number=53)