#TODO: Plot probability histograms for all Cell_IDs from optimized_type1_ver4.txt file:

def PlotProbabHist(data_file):
    cell_ID = []
    category = []
    probability = []
    for line in open(data_file, 'r'):
        line = line.rstrip().split("\t")
        cell_ID.append(int(line[0]) + 1)        # labels from 0, so add +1 to get real cell_ID
        category.append(line[1])
        probability.append(10 ** (float(line[2])))     # get the exponential to get the probability (ranging from 0 to 1)

    print (cell_ID[0], cell_ID[-1])
    print (list(set(category)))
    print (min(probability), max(probability))


    # Divide into lists:
    names = list(set(category))
    lists = [[] for i in range(len(list(set(category))))]
    for cat, prob in zip(category, probability):
        index = None
        if cat == "P_init":
            index = 0
        if cat == "P_branch":
            index = 1
        if cat == "P_term":
            index = 2
        if cat == "P_link":
            index = 3
        lists[index].append(prob)


    # Plot the histograms:
    data_file_name = data_file.split("/")[-1]
    import matplotlib.pyplot as plt
    for name, lst in zip(names, lists):
        plt.hist(lst)
        plt.title(name + " -> " + data_file_name)
        plt.ylabel("Count of Cell_IDs")
        plt.xlabel("Probability")
        plt.savefig("/Users/kristinaulicna/Documents/Rotation_2/Cell_Competition/GenTree_AnalysisFiles/Probab_" + str(name) + "_ver4.jpeg", bbox_inches = "tight")
        plt.show()


PlotProbabHist("/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/"
               "tracker_performance_evaluation/tracks_try_50/tracks/hypotheses_type2.txt")
PlotProbabHist("/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/"
               "tracker_performance_evaluation/tracks_try_50/tracks/optimized_type2.txt")
