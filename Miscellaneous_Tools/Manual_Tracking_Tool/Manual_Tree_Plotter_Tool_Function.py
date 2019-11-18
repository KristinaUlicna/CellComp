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

    # Check if frame_divisions list (=argument) has a length of 31 (=captures all cells up to 5 generations):
    if len(frames_divisions) != 31:
        raise Exception("Warning, frame_divisions list is incomplete!\n"
                        "Length of {} while it should be 31!\n"
                        "Please input data for all generations up to gen#5 to proceed.\n"
                        "\tNote: Insert None (boolean, not string = 'None') if the cell did not undergo division event.")

    # Make sure your None gets converted to the movie_length integer:
    frm = [int(item) if item is not None else movie_length for item in frames_divisions]

    # TODO: Incorporate the conditions for apoptosis / migration out of FOV:

    color_list = ["dodgerblue", "darkorange", "forestgreen", "firebrick", "gold", "plum"]


    # VERTICAL Lines:

    # Gen#0:
    plt.plot([0, 0], [1, frm[0]], color=color_list[0], marker="o")

    # Gen#1:
    if frm[0] != movie_length:
        plt.plot([-34, -34], [frm[0] + 1, frm[1]], color=color_list[1], marker="o")
    if frm[0] != movie_length:
        plt.plot([34, 34], [frm[0] + 1, frm[2]], color=color_list[1], marker="o")

    # Gen#2:
    if frm[0] != movie_length and frm[1] != movie_length:
        plt.plot([-50, -50], [frm[1] + 1, frm[3]], color=color_list[2], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length:
        plt.plot([-18, -18], [frm[1] + 1, frm[4]], color=color_list[2], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length:
        plt.plot([18, 18], [frm[2] + 1, frm[5]], color=color_list[2], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length:
        plt.plot([50, 50], [frm[2] + 1, frm[6]], color=color_list[2], marker="o")

    # Gen#3:
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length:
        plt.plot([-58, -58], [frm[3] + 1, frm[7]], color=color_list[3], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length:
        plt.plot([-42, -42], [frm[3] + 1, frm[8]], color=color_list[3], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length:
        plt.plot([-26, -26], [frm[4] + 1, frm[9]], color=color_list[3], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length:
        plt.plot([-10, -10], [frm[4] + 1, frm[10]], color=color_list[3], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length:
        plt.plot([10, 10], [frm[5] + 1, frm[11]], color=color_list[3], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length:
        plt.plot([26, 26], [frm[5] + 1, frm[12]], color=color_list[3], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length:
        plt.plot([42, 42], [frm[6] + 1, frm[13]], color=color_list[3], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length:
        plt.plot([58, 58], [frm[6] + 1, frm[14]], color=color_list[3], marker="o")

    # Gen#4:
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[7] != movie_length:
        plt.plot([-62, -62], [frm[7] + 1, frm[15]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[7] != movie_length:
        plt.plot([-54, -54], [frm[7] + 1, frm[16]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[8] != movie_length:
        plt.plot([-46, -46], [frm[8] + 1, frm[17]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[8] != movie_length:
        plt.plot([-38, -38], [frm[8] + 1, frm[18]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[9] != movie_length:
        plt.plot([-30, -30], [frm[9] + 1, frm[19]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[9] != movie_length:
        plt.plot([-22, -22], [frm[9] + 1, frm[20]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[10] != movie_length:
        plt.plot([-14, -14], [frm[10] + 1, frm[21]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[10] != movie_length:
        plt.plot([-6, -6], [frm[10] + 1, frm[22]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[11] != movie_length:
        plt.plot([6, 6], [frm[11] + 1, frm[23]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[11] != movie_length:
        plt.plot([14, 14], [frm[11] + 1, frm[24]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[12] != movie_length:
        plt.plot([22, 22], [frm[12] + 1, frm[25]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[12] != movie_length:
        plt.plot([30, 30], [frm[12] + 1, frm[26]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[13] != movie_length:
        plt.plot([38, 38], [frm[13] + 1, frm[27]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[13] != movie_length:
        plt.plot([46, 46], [frm[13] + 1, frm[28]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[14] != movie_length:
        plt.plot([54, 54], [frm[14] + 1, frm[29]], color=color_list[4], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[14] != movie_length:
        plt.plot([62, 62], [frm[14] + 1, frm[30]], color=color_list[4], marker="o")

    # Gen#5:
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[7] != movie_length and frm[15] != movie_length:
        plt.plot([-64, -64], [frm[15] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[7] != movie_length and frm[15] != movie_length:
        plt.plot([-60, -60], [frm[15] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[7] != movie_length and frm[16] != movie_length:
        plt.plot([-56, -56], [frm[16] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[7] != movie_length and frm[16] != movie_length:
        plt.plot([-52, -52], [frm[16] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[8] != movie_length and frm[17] != movie_length:
        plt.plot([-48, -48], [frm[17] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[8] != movie_length and frm[17] != movie_length:
        plt.plot([-44, -44], [frm[17] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[8] != movie_length and frm[18] != movie_length:
        plt.plot([-40, -40], [frm[18] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[8] != movie_length and frm[18] != movie_length:
        plt.plot([-36, -36], [frm[18] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[9] != movie_length and frm[19] != movie_length:
        plt.plot([-32, -32], [frm[19] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[9] != movie_length and frm[19] != movie_length:
        plt.plot([-28, -28], [frm[19] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[9] != movie_length and frm[20] != movie_length:
        plt.plot([-24, -24], [frm[20] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[9] != movie_length and frm[20] != movie_length:
        plt.plot([-20, -20], [frm[20] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[10] != movie_length and frm[21] != movie_length:
        plt.plot([-16, -16], [frm[21] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[10] != movie_length and frm[21] != movie_length:
        plt.plot([-12, -12], [frm[21] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[10] != movie_length and frm[22] != movie_length:
        plt.plot([-8, -8], [frm[22] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[10] != movie_length and frm[22] != movie_length:
        plt.plot([-4, -4], [frm[22] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[11] != movie_length and frm[23] != movie_length:
        plt.plot([4, 4], [frm[23] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[11] != movie_length and frm[23] != movie_length:
        plt.plot([8, 8], [frm[23] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[11] != movie_length and frm[24] != movie_length:
        plt.plot([12, 12], [frm[24] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[3] != movie_length and frm[11] != movie_length and frm[24] != movie_length:
        plt.plot([16, 16], [frm[24] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[12] != movie_length and frm[25] != movie_length:
        plt.plot([20, 20], [frm[25] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[12] != movie_length and frm[25] != movie_length:
        plt.plot([24, 24], [frm[25] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[12] != movie_length and frm[26] != movie_length:
        plt.plot([28, 28], [frm[26] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[1] != movie_length and frm[4] != movie_length and frm[12] != movie_length and frm[26] != movie_length:
        plt.plot([32, 32], [frm[26] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[13] != movie_length and frm[27] != movie_length:
        plt.plot([36, 36], [frm[27] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[13] != movie_length and frm[27] != movie_length:
        plt.plot([40, 40], [frm[27] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[13] != movie_length and frm[28] != movie_length:
        plt.plot([44, 44], [frm[28] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[5] != movie_length and frm[13] != movie_length and frm[28] != movie_length:
        plt.plot([48, 48], [frm[28] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[14] != movie_length and frm[29] != movie_length:
        plt.plot([52, 52], [frm[29] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[14] != movie_length and frm[29] != movie_length:
        plt.plot([56, 56], [frm[29] + 1, movie_length], color=color_list[5], marker="o")

    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[14] != movie_length and frm[30] != movie_length:
        plt.plot([60, 60], [frm[30] + 1, movie_length], color=color_list[5], marker="o")
    if frm[0] != movie_length and frm[2] != movie_length and frm[6] != movie_length and frm[14] != movie_length and frm[30] != movie_length:
        plt.plot([64, 64], [frm[30] + 1, movie_length], color=color_list[5], marker="o")


    # HORIZONTAL LINES:
    # Gen#1:
    if frm[0] != movie_length:
        plt.plot([-34, 34], [frm[0], frm[0]], color="darkgrey", marker="o", markersize=5, zorder=1)

    # Gen#2:
    if frm[1] != movie_length:
        plt.plot([-50, -18], [frm[1], frm[1]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[2] != movie_length:
        plt.plot([18, 50], [frm[2], frm[2]], color="darkgrey", marker="o", markersize=5, zorder=1)

    # Gen#3:
    if frm[3] != movie_length:
        plt.plot([-58, -42], [frm[3], frm[3]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[4] != movie_length:
        plt.plot([-26, -10], [frm[4], frm[4]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[5] != movie_length:
        plt.plot([10, 26], [frm[5], frm[5]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[6] != movie_length:
        plt.plot([42, 58], [frm[6], frm[6]], color="darkgrey", marker="o", markersize=5, zorder=1)

    # Gen#4:
    if frm[7] != movie_length:
        plt.plot([-62, -54], [frm[7], frm[7]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[8] != movie_length:
        plt.plot([-46, -38], [frm[8], frm[8]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[9] != movie_length:
        plt.plot([-30, -22], [frm[9], frm[9]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[10] != movie_length:
        plt.plot([-14, -6], [frm[10], frm[10]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[11] != movie_length:
        plt.plot([6, 14], [frm[11], frm[11]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[12] != movie_length:
        plt.plot([22, 30], [frm[12], frm[12]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[13] != movie_length:
        plt.plot([38, 46], [frm[13], frm[13]], color="darkgrey", marker="o", markersize=5, zorder=1)
    if frm[14] != movie_length:
        plt.plot([54, 62], [frm[14], frm[14]], color="darkgrey", marker="o", markersize=5, zorder=1)

    # Gen#5:
    # TODO: Update this!


    # Other stuff:
    plt.text(x=17, y=-15, s="Root ID #{}".format(root_ID), bbox=dict(facecolor=color_list[0], alpha=0.5),
             horizontalalignment='center', verticalalignment='center')
    plt.xlim(-75, 75)
    plt.ylim(-75, movie_length + 75)
    plt.ylabel("Absolute time [frames]")
    plt.title("Semi-Automated Plotter - Manual Tracking; <'17_07_24' & 'pos13'>")
    #plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/manual_tracking/Manual_GenTree_CellID_{}.jpeg".format(root_ID), bbox_inches="tight")
    plt.show()
    plt.close()



# TODO: Feature requests:
# Legend    - full line = CCT known
#           - dashed line = root / leaf cell
# Leaf      - non-filled marker dot
# Non-leaf  - full marker dot

# TODO: DO NOT PLOT THE CELL UNTIL THE END OF THE MOVIE IF IT DIED (apoptosis) OR LEFT (out of field of view)
