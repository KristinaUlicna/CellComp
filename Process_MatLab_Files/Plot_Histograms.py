# Create dictionary & list of division times:
cells_dict = {}         # key = cellID, value = first & last frame
for order, line in enumerate(open('/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracks_pos2_ID_sorted.csv', 'r')):
    line = line.rstrip().split(',')
    if int(line[3]) not in cells_dict:
        cells_dict[int(line[3])] = [int(line[2]), None]     # in minutes
    cells_dict[int(line[3])][1] = int(line[2])
print (cells_dict)
div_time_frame = [(item[1] - item[0]) for item in list(cells_dict.values())]
print (len(div_time_frame), div_time_frame)


# CATEGORIZE CELLS: Exclude cells which only appear in a SINGLE frame:
div_time_real = [item * 4 for item in div_time_frame if item != 0]
print (len(div_time_real), div_time_real)
single_frame_cells = len(div_time_frame) - len(div_time_real)
print ("Single", single_frame_cells)


# CATEGORIZE CELLS: Round up the minimums and maximums & create bins:
base = 100
maximum = base * round(max(div_time_real) / base)
print ("Min: {}".format(min(div_time_real)), '\t', "Max: {}".format(max(div_time_real)), '\t', "New Max: {}".format(maximum))
bins = list(range(0, int(maximum), base))
print ("Bins: {}".format(bins))


# CATEGORIZE CELLS: Loop through division times to categorize into bins:
bins_value = [0] * len(bins)
print ("Value {}".format(bins_value))

for div_time in div_time_real:
    index = 0
    while index <= len(bins) - 2:
        if int(div_time) > bins[index] and int(div_time) <= bins[index + 1]:
            bins_value[index] += 1
            break
        else:
            index += 1

print ("Value {}".format(bins_value))
print (len(bins_value), sum(bins_value))


# PLOT THE HISTOGRAM:
import matplotlib.pyplot as plt
plt.hist(div_time_real, bins=len(bins))
plt.title("Histogram of cell cycle times captured by S&T'd movies")
plt.xlabel("Cell Division time [mins]")
plt.ylabel("Count per category [cells]")
plt.ylim(-100)

slice_st, slice_en = 0, 9
plt.bar(div_time_real[slice_st:slice_en], bins_value[slice_st:slice_en])
plt.title("SLICE: Histogram of cell cycle times captured by S&T'd movies")
plt.xlabel("Cell Division time [mins]")
plt.ylabel("Count per category [cells]")
plt.ylim(-100)

plt.show()
plt.close()