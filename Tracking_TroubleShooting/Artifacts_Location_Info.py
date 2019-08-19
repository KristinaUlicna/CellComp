import json
import matplotlib.pyplot as plt

x_axis = []
y_axis = []

for ID in list(range(1, 1237, 1)):
    file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracks/tracks_RFP/track_{}_RFP.json".format(ID)
    try:
        with open(file) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                if key == 'x':
                    x_axis.append(value[0])
                if key == 'y':
                    y_axis.append(value[0])
    except:
        print (file)
        continue

print (x_axis)
print (y_axis)

# TODO: ATTENTION!
x_axis_true = y_axis
y_axis_true = [1200 - item for item in x_axis]

print (x_axis_true)
print (y_axis_true)


for cell in list(range(21, 51, 1)):
    fig = plt.figure(figsize=(8, 6))
    plt.plot(x_axis_true[0:20], y_axis_true[0:20], 'ob', label="Cells")
    plt.plot(x_axis_true[cell-1], y_axis_true[cell-1], 'xr', label="Cell #{}".format(cell))
    plt.xlim(0, 1600)
    plt.ylim(0, 1200)
    plt.legend()
    plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/manual_tracking/Tracker_Labels_Cell{}.jpeg".format(cell), bbox_inches="tight")
    plt.show()
plt.close()