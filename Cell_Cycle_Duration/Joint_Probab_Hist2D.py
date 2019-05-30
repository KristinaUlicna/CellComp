import matplotlib.pyplot as plt

# STEP 1: Plot an example histogram with 2 data pairs:

parent = [13.13, 12.6]
child = [12.6, 16.33]


plt.hist2d(x=parent, y=child, bins=10, zorder=1)
plt.title("Joint Probability 2D Histogram")
plt.xlabel("Parent division time")
plt.ylabel("Child division time")


# STEP 2: Make a non-layered dictionary of {parent: [child_1,, child_2]} from 'cellIDdetails_raw.txt' file:
#                                          (this is their division time)
"""
filtered_file = "/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos6/cellIDdetails_filtered.txt"

def FindCellParent(cellID):
    raw_file = filtered_file.replace("filtered", "raw")
    finding = False  # 'finding' is a marker => from this moment, look for 0 (so it doesn't return first 0 in file)
    for line in open(raw_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or len(line) < 8:
            continue
        if int(line[0]) == cellID:
            finding = True
            generation = int(line[5])
        if finding is True and int(line[5]) == generation - 1:
            finding = False
            if generation > 1:
                return [int(line[0]), float(line[4])]
            else:
                return [int(line[0]), "NaN"]
"""
# Call the function - create a dictionary:
"""
dictionary = {}

for line in open(filtered_file, 'r'):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 8:
        continue
    cell_name = int(line[0])
    cell_time = float(line[4])
    parent_info = FindCellParent(cellID=cell_name)
    parent_cell, parent_time = parent_info[0], parent_info[1]
    if parent_time != "NaN" and isinstance(parent_time, float):
        dictionary[parent_cell, parent_time] = [cell_name, cell_time]
       
print ("Dictionary -> len: {}; {}".format(len(dictionary), dictionary))
"""
# Call the function - create 2 lists:
"""
x_axis_list = []
y_axis_list = []

for line in open(filtered_file, 'r'):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 8:
        continue
    cell_name = int(line[0])
    cell_time = float(line[4])
    parent_info = FindCellParent(cellID=cell_name)
    parent_cell, parent_time = parent_info[0], parent_info[1]
    if parent_time != "NaN" and isinstance(parent_time, float):
        x_axis_list.append(parent_time)
        y_axis_list.append(cell_time)

print("Parent time list -> len: {}; {}".format(len(x_axis_list), x_axis_list))
print("CellID time list -> len: {}; {}".format(len(y_axis_list), y_axis_list))
"""
# STEP 3: Extract the CCT[h] to make axes from the dictionary:
"""
x_axis = []
y_axis = []
for key, value in dictionary.items():
    x_axis.append(key[1])
    y_axis.append(value[1])
"""
"""
n_bins = list(range(12, 22 + 1, 1))
plt.hist2d(x=x_axis_list, y=y_axis_list, bins=n_bins)
plt.title("Joint Probability 2D Histogram")
plt.xlabel("Parent division time")
plt.ylabel("Child division time")
plt.show()
plt.close()


# STEP 4: Do sanity check for overwriting:

counter = 0
for line in open(filtered_file, 'r'):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 8:
        continue
    if int(line[5]) > 1:
        print (line)
        counter += 1
print ("Counter: {}".format(counter))
print (len(x_axis_list) == len(y_axis_list) == counter)

# TODO: Do this for merged data!
"""
data = [13.0, 13.1]

plt.plot(data, data, "r-", zorder=2)
plt.show()
plt.close()
