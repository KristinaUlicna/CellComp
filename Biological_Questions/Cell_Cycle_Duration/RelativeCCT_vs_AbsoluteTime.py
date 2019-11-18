import matplotlib.pyplot as plt
import sys
sys.path.append("../")

from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


def PlotScatterCCTvsAbsTime(exp_type="MDCK_WT_Pure"):
    _, txt_file_list = GetMovieFilesPaths(exp_type=exp_type)
    color_list = ["blue", "orange", "green", "red", "yellow", "blue", "orange", "green", "red", "yellow",
                  "blue", "orange", "green", "red", "yellow", "blue", "orange", "green", "red", "yellow", "violet"]

    for color, filtered_file in zip(color_list, txt_file_list):
        filtered_file = filtered_file.replace("raw", "filtered")
        print("Filtered File: {}".format(filtered_file))
        file = filtered_file.split("/")[-4] + "-" + filtered_file.split("/")[-3]

        # Categorize CCT & frame of the division start according to the generations:
        generation_list = [[]]
        for line in open(filtered_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] == "Cell_ID":
                continue
            gen = int(line[5])
            cct = int(line[3])    # cell cycle duration in mins
            frm = int(line[1])    # frame when the cell is born
            if gen > len(generation_list):  # append by as many empty lists as are missing!
                generation_list.append(([] * (gen - len(generation_list))))
            generation_list[gen - 1].append([cct,frm])

        # Print summary:
        gen_list = []
        for gen in generation_list:
            gen_list.append(len(gen))
        print ("Generations total = {}; Length of sub-lists = {}; Whole gen list = {}" \
               .format(len(generation_list), gen_list, generation_list))

        alpha_list = [0.25, 0.4, 0.55, 0.7]

        # Iterate through the files to make plots:
        for number, gen in enumerate(generation_list):
            for datapoint in gen:
                plt.scatter(x=datapoint[1], y=datapoint[0], marker='x', color=color, alpha=alpha_list[number])
            # To set a label, plot the thing away from the display limits so it doesn't appear:
            if number == 0:
                plt.scatter(-500, -500, marker='x', color=color, alpha=0.7,
                            label="File {}".format(file))

    # Plot one big figure instead of 21 separate plots!
    plt.title("Whole 'MDCK_WT_Pure' dataset\n21 movies (filtered merged data)")
    plt.xlim(-100, 1300)
    plt.xlabel("Absolute movie time [frames]")
    plt.ylim(-200, 3200)
    plt.ylabel("Relative cell doubling time [mins]")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("/Volumes/lowegrp/Data/Kristina/{}/Scatter_RelCCT_vs_AbsFrames.jpeg".format(exp_type), bbox_inches="tight")
    plt.show()
    plt.close()


PlotScatterCCTvsAbsTime()