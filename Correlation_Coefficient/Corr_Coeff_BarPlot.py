# TODO: Plot a barplot for calculated correlation coefficients:

import matplotlib.pyplot as plt
import sys
sys.path.append("../")

from Correlation_Coefficient.Correl_Coeff_Calc_Plots_Class_All import Correlation
from Correlation_Coefficient.Correl_Coeff_Calc_Plots_Class_Outliers import Correlation_Outliers


# Call the class:
corr_coeff_list = []
for x, y in zip(["Parent", "Grandparent", "Sibling_1"], ["Child", "Grandchild", "Sibling_2"]):
    corr = Correlation(x_type=x, y_type=y)
    coeff = corr.CalculateCorrCoeff()
    corr_coeff_list.append(coeff)
    for outlier in ["left", "middle", "right"]:
        call = Correlation_Outliers(x_type=x, y_type=y, left_or_right=outlier)
        coeff = call.CalculateCorrCoeff()
        corr_coeff_list.append(coeff)

print(corr_coeff_list)
corr_coeff_list[7] = 0.0


# Plot a barplot:
category = ["All Cells", "Fast Dividers", "Normal Dividers", "Slow Dividers"] * 3

plt.bar(x=category, height=corr_coeff_list)
plt.xticks(rotation=45)
plt.ylabel("Correlation Coefficient")
plt.title("Correlation Coefficients of Cell Pairs in Lineage Trees")
plt.grid(axis='y')
plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/correlations/Correlation_Coefficients_BarPlot.jpeg", bbox_inches="tight")
plt.show()
plt.close()
