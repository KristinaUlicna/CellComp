import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("../")

from Cell_Local_Density.Correl_Density_CCT import CorrelationDenCCT

# Call the function & plot the barplot:
coe_b = CorrelationDenCCT(density_span="birth")
coe_o = CorrelationDenCCT(density_span="one_quarter")
coe_h = CorrelationDenCCT(density_span="half_way")
coe_t = CorrelationDenCCT(density_span="three_quarters")
coe_m = CorrelationDenCCT(density_span="mitosis")
labels = ["Gen#1", "Gen#2", "Gen#3", "Across"]

x = np.arange(len(labels))      # the label locations
width = 0.15                     # the width of the bars

fig, ax = plt.subplots()
ax.bar(x - 2*width, coe_b, width, alpha=0.6, label='Birth')
ax.bar(x - width, coe_o, width, alpha=0.6, label='1/4')
ax.bar(x, coe_h, width, alpha=0.6, label='Half')
ax.bar(x + width, coe_t, width, alpha=0.6, label='3/4')
ax.bar(x + 2*width, coe_m, width, alpha=0.6, label='Divis')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Correlation Coefficient')
ax.set_title('Correlation Coefficient by Timepoint and Generation')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), ncol=5)
ax.grid(b=None, which='major', axis='y')

plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Correlation_Barplots/Density_Vs_CCT.jpeg", bbox_inches="tight")
plt.show()
plt.close()