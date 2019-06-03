# TODO: Figure out how many cell_IDs are artefacts:
# Use 'cellIDdetails_raw.txt' file for this!

def FigureOutTrimmingLimit(txt_file, print_stats=False):
    """ Find out the percentage of lines which contain cellID artefacts. """

    file_len = sum(1 for line in open(txt_file)) - 2
    trimming_limit = [1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 75]    # no. of frames
    trimming_limit_line_count = [0 for _ in range(len(trimming_limit))]
    omg_counter = 0
    for line in open(txt_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] == "Cell_ID" or len(line) < 8:
            continue
        # Play with the trimming limit (frames):
        for order, limit in enumerate(trimming_limit):
            if float(line[3]) < limit * 4:
                trimming_limit_line_count[order] += 1
        if int(line[5]) != 0 and float(line[3]) < trimming_limit[-1] * 4:
            omg_counter += 1

    if print_stats is True:
        print ("Raw file: length: {} -> {}".format(file_len, txt_file))
        for limit, line_count in zip(trimming_limit, trimming_limit_line_count):
            print ("Trimming limit: {} frames\t(= {} minutes, {} hours)\t-> line count = {}"
                   .format(limit, limit * 4, round(limit * 4 / 60, 2), line_count))
        print ("OMG counter: (under {} frames or {} hours) {}"
               .format(trimming_limit[-1], trimming_limit[-1] * 4 / 60, omg_counter))


FigureOutTrimmingLimit("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/Example_Movie/17_07_24-pos6/cellIDdetails_raw.txt", print_stats=True)