import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("../")

from Correlation_Coefficient.Relationship_CCT_Correl_Class import Correlation

corr_par = []
for subcat in ["all", "left", "middle", "right"]:
    call = Correlation(x_type="Parent", y_type="Child", category=subcat)
    call.CalculateCorrCoeff()
    corr_par.append(call.coeff)

corr_sib = []
for subcat in ["all", "left", "middle", "right"]:
    call = Correlation(x_type="Sibling", y_type="Sibling", category=subcat)
    call.CalculateCorrCoeff()
    corr_sib.append(call.coeff)

print ("Correlation Coefficients for Par & Chld: {}".format(corr_par))
print ("Correlation Coefficients for Sib & Sib: {}".format(corr_sib))


# Plot a barplot:
# TODO: Add labels to see how many cell pairs you analysed!
# Instructions: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

labels = ["All Cells", "Fast Dividers", "Normal Dividers", "Slow Dividers"]
x = np.arange(len(labels))       # the label locations
width = 0.4                      # the width of the bars

fig, ax = plt.subplots()
ax.bar(x - width/2, corr_par, width, alpha=0.6, label='Parent-Child')
ax.bar(x + width/2, corr_sib, width, alpha=0.6, label='Sibling-Sibling')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Correlation Coefficient')
ax.set_title('Correlation Coefficient by Lineage Relationship and Division Subcategory')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), ncol=5)
ax.grid(b=None, which='major', axis='y')

plt.savefig("/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Correlation_Barplots/CCT_Vs_CCT.jpeg", bbox_inches="tight")
plt.show()
plt.close()
