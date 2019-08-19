#TODO: Plot the R^2 onto a graph:

import matplotlib.pyplot as plt
import sys
sys.path.append("../")

from scipy.stats import linregress
from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths


def ModelLinRegress(raw_txt_file_list, percentage):
    """ Function to model the relationship between the cell cycle duration and cell density
        using linear regression at each percentage point of the cell-IS's life time.

    Args:
        raw_txt_file_list (list of str) ->  list of absolute paths to all 'cellIDdetails_raw.txt' files
                                                in a certain exp_type (e.g. 'MDCK_WT_Pure')
                                                the function automatically converts the directories
                                                to '/density/cellID_density.txt' to access density dictionaries.
        percentage (int)                -> percentage point for which you want the linear regression to be calculated
                                                from smoothed density data; ranges from 1% to 100%
    Return:
        cct_hrs_list (list of floats)   -> total cell cycle duration of certain cell-ID
        den_per_list (list of floats)   -> estimate of cell density at the given % point of certain cell-ID
                    lists have equal length and can be plotted as scatter plots to see dependencies...
    """

    if percentage < 1 or percentage > 100:
        raise Exception("Warning, percentage range should be only between 1% & 100%!")

    cct_hrs_list = []
    den_per_list = []

    for raw_file in raw_txt_file_list:
        smoothed_density_file = raw_file.split("/")[:-2]
        smoothed_density_file = "/".join(smoothed_density_file) + "/density/cellID_density_smoothed.txt"

        for line in open(smoothed_density_file, 'r'):
            line = line.rstrip().split("\t")
            if line[0] != "Cell_ID":
                if float(line[1]) < 8.00:
                    print ("Cell_ID {} lives for less than 8.0 hours. Excluded from analysis.\nFile name: {}"
                           .format(line[0], smoothed_density_file))
                    continue
                cct_hrs_list.append(float(line[1]))
                den_per_list.append(float(line[percentage+1]))

    den_per_list = [item * 10000 for item in den_per_list]
    return cct_hrs_list, den_per_list


# Call the function:
_, txt_file_list = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")

x = list(range(1, 101, 1))
slope_list = []
intrc_list = []
r_sqr_list = []

"""
slope       : slope of the regression line
intercept   : intercept of the regression line
r-value     : correlation coefficient
p-value     : two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero
stderr      : standard error of the estimate
"""

for perc in x:
    print ("Currently on {}%...".format(perc))
    cct_hrs_list, den_per_list = ModelLinRegress(raw_txt_file_list=txt_file_list, percentage=perc)
    result = linregress(cct_hrs_list, den_per_list)
    slope_list.append(result[0])
    intrc_list.append(result[1])
    r_sqr_list.append(result[2]**2)
    if perc == 25 or perc == 50 or perc == 75:
        plt.scatter(x=cct_hrs_list, y=den_per_list, color="tomato", alpha=0.3, label="Cell-ID datapoints")
        plt.plot([-10, 60], [result[0]*-10+result[1], result[0]*60+result[1]], color="grey",
                 linestyle='dashed', linewidth=2, label="Regression line")
        plt.xlim(0, 50)
        plt.ylim(0, 18)
        plt.title("Example Cell Cycle Duration vs. Cell Density Data at {}% of Life Time".format(perc))
        plt.xlabel("Cell Cycle Duration [hours]")
        plt.ylabel("Cell Density [μm^-2 x 10^-4]")
        plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/regression_lines/{}_percent_dataset.jpeg".format(perc),
                    bbox_inches="tight")
        plt.show()
        plt.close()


# Plot the thing on the scatter:

    # Correlation of determination:
plt.scatter(x=x, y=r_sqr_list, color="firebrick")
plt.xticks(list(range(0, 101, 10)))
plt.xlabel("Percentage of Cell Cycle [%]")
plt.ylabel("Coefficient of determination (R^2)")
plt.title("Correlation between Cell Cycle Duration & Density\nacross Life Time [%] on Smoothed Cell Density data")
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/regression_lines/Correlation_Coefficient_100percent.jpeg", bbox_inches="tight")
plt.show()
plt.close()

    # Slope of the curve:
plt.scatter(x=x, y=slope_list, color="dodgerblue")
plt.xticks(list(range(0, 101, 10)))
plt.xlabel("Percentage of Cell Cycle [%]")
plt.ylabel("Regression Line Characteristics")
plt.title("Slope of the Regression Line\nfitted on Cell Cycle Duration & Density data")
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/regression_lines/Regression_Line_Slope_100percent.jpeg", bbox_inches="tight")
plt.show()
plt.close()

    # Intercept of the curve:
plt.scatter(x=x, y=intrc_list, color="forestgreen")
plt.xticks(list(range(0, 101, 10)))
plt.xlabel("Percentage of Cell Cycle [%]")
plt.ylabel("Regression Line: Intercept")
plt.title("Intercept of the Regression Line\nfitted on Cell Cycle Duration & Density data")
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/regression_lines/Regression_Line_Intercept_100percent.jpeg", bbox_inches="tight")
plt.show()
plt.close()

