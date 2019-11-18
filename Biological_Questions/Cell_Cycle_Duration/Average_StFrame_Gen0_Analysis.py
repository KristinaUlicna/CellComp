# TODO: You have 1973 cells in generation#1, i.e. 1973 parent cells (each should be mentioned twice) Analyse these!

import matplotlib.pyplot as plt

gen_0_file = "/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_parents_gen0.txt"

frames_gen_0 = []
cell_ID_gen_0 = []

for line in open(gen_0_file, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID-posX-date" or len(line) < 8:
        continue
    frames_gen_0.append([int(line[1]), int(line[2])])   # x-axis
    cell_ID_gen_0.append([int(line[0].split("-")[0]), int(line[0].split("-")[0])])  # y-axis


frames_gen_1 = []
cell_ID_gen_1 = []
frames_gen_2 = []
cell_ID_gen_2 = []
frames_gen_3 = []
cell_ID_gen_3 = []

gen_file = "/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_merged.txt"

for line in open(gen_file, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID-posX-date" or len(line) < 8:
        continue
    if int(line[5]) == 1:
        frames_gen_1.append([int(line[1]), int(line[2])])   # x-axis
        cell_ID_gen_1.append([int(line[0].split("-")[0]), int(line[0].split("-")[0])])  # y-axis
    if int(line[5]) == 2:
        frames_gen_2.append([int(line[1]), int(line[2])])   # x-axis
        cell_ID_gen_2.append([int(line[0].split("-")[0]), int(line[0].split("-")[0])])  # y-axis
    if int(line[5]) == 3:
        frames_gen_3.append([int(line[1]), int(line[2])])   # x-axis
        cell_ID_gen_3.append([int(line[0].split("-")[0]), int(line[0].split("-")[0])])  # y-axis



# Mean start & end frame of gen#0 of analysed cells:
mean_st_frame_gen_0 = 0
mean_en_frame_gen_0 = 0
for item in frames_gen_0:
    mean_st_frame_gen_0 += item[0]
    mean_en_frame_gen_0 += item[1]
mean_st_frame_gen_0 = mean_st_frame_gen_0 / len(frames_gen_0)
mean_en_frame_gen_0 = mean_en_frame_gen_0 / len(frames_gen_0)

print ("St_frame_gen_0: mean = {}; {} hours".format(mean_st_frame_gen_0, mean_st_frame_gen_0 * 4 / 60))
print ("En_frame_gen_0: mean = {}, {} hours".format(mean_en_frame_gen_0, mean_en_frame_gen_0 * 4 / 60))

print ((mean_st_frame_gen_0 * 4 / 60) - (mean_en_frame_gen_0 * 4 / 60))


# Plot the gen#0 only:
"""
for order, cell in enumerate(zip(frames_gen_0, cell_ID_gen_0)):
    plt.plot(frames_gen_0[order], cell_ID_gen_0[order], alpha=0.3)
plt.xlim(-50, 1850)
plt.title("Lifetime of Generation#0: parents of analysed gen#1 cells")
plt.xlabel("Frame #")
plt.ylabel("Cell_ID label")

directory = gen_0_file.split("/")[:-1]
directory = "/".join(directory)
plt.savefig(directory + "/Plot_LifeTime_Gen0_Parents.jpeg", bbox_inches="tight")

plt.show()
plt.close()
"""

# Plot all available generations:
for order, _ in enumerate(zip(frames_gen_0, cell_ID_gen_0)):
    plt.plot(frames_gen_0[order], cell_ID_gen_0[order], color="red", alpha=0.3)

for order, _ in enumerate(zip(frames_gen_1, cell_ID_gen_1)):
    plt.plot(frames_gen_1[order], cell_ID_gen_1[order], color="blue", alpha=0.3)

for order, _ in enumerate(zip(frames_gen_2, cell_ID_gen_2)):
    plt.plot(frames_gen_2[order], cell_ID_gen_2[order], color="orange", alpha=0.3)

for order, _ in enumerate(zip(frames_gen_3, cell_ID_gen_3)):
    plt.plot(frames_gen_3[order], cell_ID_gen_3[order], color="green", alpha=0.3)

plt.title("Generation #0 - Generation #3 Cell-ID lifetimes")
plt.ylim(-200, 12200)
plt.ylabel("Cell-ID label")
plt.xlim(-50, 1550)
plt.xlabel("Frame #")
plt.legend()

directory = gen_0_file.split("/")[:-1]
directory = "/".join(directory)
plt.savefig(directory + "/Plot_LifeTime_Gen0toGen3.jpeg", bbox_inches="tight")
plt.show()
plt.close()
