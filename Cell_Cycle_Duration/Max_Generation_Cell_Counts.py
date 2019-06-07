# TODO: Find out whether the cells which are in generation 4 or 5 are actually there due to short CCT:

merged_file = "/Users/kristinaulicna/Documents/Rotation_2/cellIDdetails_merged.txt"

counter = [0 for _ in range(6)]
for line in open(merged_file, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID-posX-date":
        continue
    generation = int(line[5])
    counter[generation] += 1
    if generation == 4:
        print (line)

print (counter)
