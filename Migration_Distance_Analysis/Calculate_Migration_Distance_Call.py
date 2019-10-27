import numpy as np
import matplotlib.pyplot as plt

from Migration_Distance_Analysis.Calculate_Migration_Distance_Function import ExtractMigrationDistances

cell_ID_list, distance_list = ExtractMigrationDistances()

migration_data = []
for cell_ID, distances in zip(cell_ID_list, distance_list):
    averages = [np.mean(distances), np.std(distances), np.median(distances), np.sum(distances), len(distances)]
    migration_data.append([round(item, 4) for item in averages])
    if np.mean(distances) > 5.00:
        print ("Cell_ID #{} migrated {} pixels on averege (±{} st.dev). It lived for {} frames... Min = {}; max = {}"
               .format(cell_ID, migration_data[-1][0], migration_data[-1][1],
                       len(distances), min(distances), max(distances)))

# Process the large list:
#mean_list, stdv_list, medn_list, sums_list, frms_list = [], [], [], [], []
data_list = [[] for _ in range(5)]
for mini_list in migration_data:
    index = 0
    while index < 5:
        data_list[index].append(mini_list[index])
        index += 1

# Plot the means on the histogram:
print (migration_data)
print (len(migration_data))
print (data_list)
print (len(data_list))

for mini in data_list:
    print (mini)

a, b, c = plt.hist(data_list[0], bins=6, range=(0.5, 3.5))
plt.title("Histogram of the MEAN distance migrated by Gen #1 MDCK WT cells")
plt.xlabel("Mean distance migrated by the cell_ID [pixels]")
plt.ylabel("Frequency of occurence")
plt.ylim(-10)
#plt.savefig(dr + "Outlier_{}_Boxplot.png".format(label), bbox_inches='tight')
plt.show()
plt.close()

print (a)
print (b)
print (c)

"""
a, b, c = plt.hist(data_list[3], bins=10, range=(0, 5))
plt.title("Histogram of the TOTAL distance migrated by Gen #1 MDCK WT cells")
plt.xlabel("Total distance migrated by the cell_ID [pixels]")
plt.ylabel("Frequency of occurence")
plt.ylim(-10)
#plt.savefig(dr + "Outlier_{}_Boxplot.png".format(label), bbox_inches='tight')
plt.show()
plt.close()

print (a)
print (b)
print (c)
"""