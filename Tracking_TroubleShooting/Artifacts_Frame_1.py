raw_file = "/Users/kristinaulicna/Documents/Rotation_2/Movie/cellIDdetails_raw.txt"

counter = 0
for line in open(raw_file, "r"):
    line = line.rstrip().split("\t")
    if line[0] == "Cell_ID" or len(line) < 5:
        continue
    if int(line[1]) == 755:
        counter += 1
        print (line)
print (counter)
