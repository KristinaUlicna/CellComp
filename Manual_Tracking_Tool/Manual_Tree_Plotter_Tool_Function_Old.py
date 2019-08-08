# TODO: Automate this if you can:
# Currently, the script plots manually-entered cell tracking data onto a scatter plot.
#       Note: This structure captures max. 4 full generations (fifth would have no room to be plotted).
# This is cell_ID #14 from '17_07_24' 'pos13' xml_file.

import matplotlib.pyplot as plt

def ManualTrackingTool(frames_divisions, root_ID, movie_length=1105, show=True):
    """ Plot a scatter plot of manually-entered cell tracking data.

    Args:
        movie_length (integer)                  Default = 1105
            -> length of the movie from which the cell originates
        frames_divisions (list of integers)
            -> list of frame number when divisions happened.
                    TO BE ORGANISED AS FOLLOWS:

    Return:
        None.
        Visualises the plot if option turned on.

    Notes:


    """

    frm = frames_divisions

    """
    x_0 = [0, 0]
    y_0 = [1, frm[0]]

    x_1 = [-34, -34, 34, 34]
    y_1 = [frm[0] + 1, frm[1], frm[0] + 1, frm[2]]

    x_2 = [-50, -50, -18, -18, 18, 18, 50, 50]
    y_2 = [frm[1] + 1, frm[3], frm[1] + 1, frm[4], frm[2] + 1, frm[5], frm[2] + 1, frm[6]]

    x_3 = [-58, -58, -42, -42, -26, -26, -10, -10, 10, 10, 26, 26, 42, 42, 58, 58]
    y_3 = [frm[3] + 1, frm[7], frm[3] + 1, frm[8],
           frm[4] + 1, frm[9], frm[4] + 1, frm[10],
           frm[5] + 1, frm[11], frm[5] + 1, frm[12],
           frm[6] + 1, frm[13], frm[6] + 1, frm[14]]

    x_4 = [-62, -62, -54, -54, -46, -46, -38, -38, -30, -30, -22, -22, -14, -14, -6, -6,
           6, 6, 14, 14, 22, 22, 30, 30, 38, 38, 46, 46, 54, 54, 62, 62]
    y_4 = [frm[7] + 1, movie_length, frm[7] + 1, movie_length,
           frm[8] + 1, movie_length, frm[8] + 1, movie_length,
           frm[9] + 1, movie_length, frm[9] + 1, movie_length,
           frm[10] + 1, movie_length, frm[10] + 1, movie_length,
           frm[11] + 1, movie_length, frm[11] + 1, movie_length,
           frm[12] + 1, movie_length, frm[12] + 1, movie_length,
           frm[13] + 1, movie_length, frm[13] + 1, movie_length,
           frm[14] + 1, movie_length, frm[14] + 1, movie_length]
    """

    color_list = ["dodgerblue", "darkorange", "forestgreen", "firebrick", "plum"]

    #for x, y in zip([x_2, x_3, x_4], [y_2, y_3, y_4]):
    #    plt.scatter(x=x, y=y)

    # VERTICAL Lines:

    # Gen#0:
    plt.plot([0, 0], [1, frm[0]], color=color_list[0], marker="o")

    # Gen#1:
    plt.plot([-34, -34], [frm[0] + 1, frm[1]], color=color_list[1], marker="o")
    plt.plot([34, 34], [frm[0] + 1, frm[2]], color=color_list[1], marker="o")

    # Gen#2:
    plt.plot([-50, -50], [frm[1] + 1, frm[3]], color=color_list[2], marker="o")
    plt.plot([-18, -18], [frm[1] + 1, frm[4]], color=color_list[2], marker="o")
    plt.plot([18, 18], [frm[2] + 1, frm[5]], color=color_list[2], marker="o")
    plt.plot([50, 50], [frm[2] + 1, frm[6]], color=color_list[2], marker="o")

    # Gen#3:
    plt.plot([-58, -58], [frm[3] + 1, frm[7]], color=color_list[3], marker="o")
    plt.plot([-42, -42], [frm[3] + 1, frm[8]], color=color_list[3], marker="o")
    plt.plot([-26, -26], [frm[4] + 1, frm[9]], color=color_list[3], marker="o")
    plt.plot([-10, -10], [frm[4] + 1, frm[10]], color=color_list[3], marker="o")
    plt.plot([10, 10], [frm[5] + 1, frm[11]], color=color_list[3], marker="o")
    plt.plot([26, 26], [frm[5] + 1, frm[12]], color=color_list[3], marker="o")
    plt.plot([42, 42], [frm[6] + 1, frm[13]], color=color_list[3], marker="o")
    plt.plot([58, 58], [frm[6] + 1, frm[14]], color=color_list[3], marker="o")

    # Gen#4:
    plt.plot([-62, -62], [frm[7] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([-54, -54], [frm[7] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([-46, -46], [frm[8] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([-38, -38], [frm[8] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([-30, -30], [frm[9] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([-22, -22], [frm[9] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([-14, -14], [frm[10] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([-6, -6], [frm[10] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([6, 6], [frm[11] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([14, 14], [frm[11] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([22, 22], [frm[12] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([30, 30], [frm[12] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([38, 38], [frm[13] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([46, 46], [frm[13] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([54, 54], [frm[14] + 1, movie_length], color=color_list[4], marker="o")
    plt.plot([62, 62], [frm[14] + 1, movie_length], color=color_list[4], marker="o")

    # HORIZONTAL LINES:
    plt.plot([-34, 34], [frm[0], frm[0]], color="silver", zorder=1)

    plt.plot([-50, -18], [frm[1], frm[1]], color="silver", zorder=1)
    plt.plot([18, 50], [frm[2], frm[2]], color="silver", zorder=1)

    plt.plot([-58, -42], [frm[3], frm[3]], color="silver", zorder=1)
    plt.plot([-26, -10], [frm[4], frm[4]], color="silver", zorder=1)
    plt.plot([10, 26], [frm[5], frm[5]], color="silver", zorder=1)
    plt.plot([42, 58], [frm[6], frm[6]], color="silver", zorder=1)

    plt.plot([-62, -54], [frm[7], frm[7]], color="silver", zorder=1)
    plt.plot([-46, -38], [frm[8], frm[8]], color="silver", zorder=1)
    plt.plot([-30, -22], [frm[9], frm[9]], color="silver", zorder=1)
    plt.plot([-14, -6], [frm[10], frm[10]], color="silver", zorder=1)
    plt.plot([6, 14], [frm[11], frm[11]], color="silver", zorder=1)
    plt.plot([22, 30], [frm[12], frm[12]], color="silver", zorder=1)
    plt.plot([38, 46], [frm[13], frm[13]], color="silver", zorder=1)
    plt.plot([54, 62], [frm[14], frm[14]], color="silver", zorder=1)

    # Other stuff:
    plt.text(x=15, y=40, s="Root ID #{}".format(root_ID), bbox=dict(facecolor=color_list[0], alpha=0.5),
             horizontalalignment='center', verticalalignment='center')
    plt.xlim(-67, 67)
    plt.ylim(-50, movie_length + 50)
    plt.ylabel("Absolute time [frames]")
    plt.title("Semi-Automated Plotter - Manual Tracking; <'17_07_24' & 'pos13'>")
    plt.show()
    plt.close()


frm = [117, 328, 333, 553, 576, 551, 596, 784, 808, 782, 792, 832, 837, 829, 853]
ManualTrackingTool(frames_divisions=frm, root_ID=5)


# TODO: Feature requests:
# Legend    - full line = CCT known
#           - dashed line = root / leaf cell
