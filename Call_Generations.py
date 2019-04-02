from Fun_Generations import GenerationTracking

#TODO: Loop through these!

files = list(range(3))
for pos in files:
    generation = GenerationTracking('/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Tracks_pos' + str(pos) + '_ID_sorted.csv')
    print ("\n\tP O S  #" + str(pos))
    print ("Total Cells: {}".format(len(generation[0]) + len(generation[1]) + len(generation[2]) + len(generation[3]) + len(generation[4]) + len(generation[5])))
    gen_names = ['Childless'] + list(range(1,6))
    for gen, name in zip(generation, gen_names):
        print ("Gen {}".format(name), ": {}".format(len(gen)), gen)

