# Define a function to check how many generations you have in the tracks:

# ---------- TODO: Some basic ASSUMPTIONS:
# 1) The daughter cell is always tracked to the same mother cell.
# 2) No consideration whether the cell completes the cell cycle prior to division.
# 3) Not checking if the 'childless' cell do not divide, die or get re-labeled.


def GenerationTracking(tracks_file):
    """Dissects the cells .csv input file into generations according to their divisions."""
    generation = [[] for i in range(6)]     # MDCK mean doubling time is ~12-30 hours so do not expect more than 6-7 generations!
    for line in open(tracks_file, 'r'):
        line = line.rstrip().split(',')
        if int(line[4]) == 0:
            generation[0].append(int(line[3]))          # all 'root' cells as seeded
        else:
            if int(line[4]) not in generation[1]:
                generation[1].append(int(line[4]))      # [1] = 1st gen
            if int(line[3]) not in generation[2]:
                generation[2].append(int(line[3]))      # [2] = 2nd gen
            # TODO: Can be done in a more elegant way:
            if int(line[4]) in generation[2]:
                generation[3].append(int(line[3]))      # [3] = 3rd gen
            if int(line[4]) in generation[3]:
                generation[4].append(int(line[3]))      # [4] = 4th gen
            if int(line[4]) in generation[4]:
                generation[5].append(int(line[3]))      # [5] = 5th gen
    generation = [sorted(list(set(gen))) for gen in generation]
    generation[0] = [cell for cell in generation[0] if cell not in generation[1]]   # [0] = 'childless'
    return generation


def StoreGenerationFile(tracks_file):
    generation = GenerationTracking(tracks_file)
    store_file = open(str(tracks_file).split("ID_sorted")[0] + "generations.tsv", 'w')
    pos = int(str(tracks_file).split("pos")[1].split("_")[0])

    index = 0
    total_cells = 0
    while index < len(generation):
        total_cells += len(generation[index])
        index += 1
    string = "POS #" + str(pos) + "\nTotal Cells:" + str(total_cells) + "\n"

    gen_names = ['Childless'] + list(range(1, len(generation)))
    for gen, name in zip(generation, gen_names):
        string += "Gen " + str(name) + " : " + str(len(gen)) + " " + str(gen) + "\t"
        string = string[:-1]
        string += "\n"
    store_file.write(string)
    store_file.close()


#TODO: Optimize the range(n) to the number of generations present in the file
#TODO: Loop through the 'if' statements in an elegant way
#TODO: Plot lineage trees (check link at: https://plot.ly/python/tree-plots/)
