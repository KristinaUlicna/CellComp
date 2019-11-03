def CheckTerminateHypothesis(config_number):
    """ Shows hypothesis which are proposed ('hypotheses_type2.txt')
        only for tracks chosen to be terminated ('optimized_type2.txt').
    """

    file_hyp = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/tracker_performance_evaluation/" \
                    "tracks_try_{}/tracks/hypotheses_type2.txt".format(config_number)
    file_opt = file_hyp.replace("hypotheses", "optimized")

    cell_ID_list = []
    options_dict = {}
    for line_opt in open(file_opt, "r"):
        line_opt = line_opt.rstrip().split("\t")
        line_opt = [int(line_opt[0].split(" ")[0]) + 1, line_opt[1].split(" ")[1], float(line_opt[2].split(" ")[1])]
        if line_opt[0] not in cell_ID_list and line_opt[1] == "Fates.TERMINATE":
            cell_ID_list.append(line_opt[0])

    for line_hyp in open(file_hyp, "r"):
        line_hyp = line_hyp.rstrip().split("\t")
        line_hyp = [int(line_hyp[0].split(" ")[0]) + 1, line_hyp[1].split(" ")[1], float(line_hyp[2].split(" ")[1])]
        cell_ID = line_hyp[0]
        option = line_hyp[1]
        if cell_ID in cell_ID_list:
            if cell_ID not in options_dict:
                options_dict[cell_ID] = [option]
                continue
            if option == "Fates.TERMINATE":
                continue
            else:
                options_dict[cell_ID].append(option)

    if len(cell_ID_list) == len(options_dict):
        return options_dict
    else:
        raise Exception("Warning: Lengths of intermediate variables do not match!"
                        "Cell_ID_List len = {}; Options_Dict len = {}".format(len(cell_ID_list), len(options_dict)))


dictionary = CheckTerminateHypothesis(config_number=50)
print (dictionary)
counter = 0
for key, value in dictionary.items():
    value.remove("Fates.FALSE_POSITIVE")
    value.remove("Fates.INITIALIZE")
    if len(value) != 0:
        print ("{}: {}".format(key, value))
        counter += 1
print (len(dictionary), counter)


