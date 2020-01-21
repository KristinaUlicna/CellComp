# TODO: Topographical 3D Surface Plot with Plotly:

import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ----- EXAMPLE DATA:
"""
# Read data from a csv
z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

fig = go.Figure(data=[go.Surface(z=z_data.values)])

fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

fig.show()
"""

# ----- REAL DATA:

mse_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE_Grid_Search.txt"

# Pair up the parameters with your actual results from the file: First, process only for amps 2.0, 2.1, 2.2
params = []
amplitude = 2.0
elev = [45, 35], [75, 60]
for amp in np.linspace(amplitude, amplitude, 1):
    for per in np.linspace(6.0, 42.0, 361):
        for shift_v in np.linspace(12.0, 24.0, 121):
            params.append([amp, per, shift_v])

# Read the file with the MSE values and extract the first 87,362 values:
results = []
for i, line in enumerate(open(mse_file, "r")):
    line = line.rstrip()
    if i == 8:                      # MSEs written in line #9!
        line = line.split("\t")
        line = [float(item) for item in line]
        results = line[43681*int(str(amplitude)[-1]):43681*(int(str(amplitude)[-1])+1)]


# Make data on 'x' & 'y' axes by using a meshgrid:
period = np.linspace(6.0, 42.0, 361)
shiftv = np.linspace(12.0, 24.0, 121)
X, Y = np.meshgrid(period, shiftv)

# Extract the data with locked amplitude:
def Find_MSE(per, sft):
    for item, mse in zip(params, results):
        if item[0] == amplitude and item[1] == per and item[2] == sft:
            return mse

Z = [[0 for i in range(X.shape[1])] for j in range(X.shape[0])]
for index_row, (row_x, row_y) in enumerate(zip(X, Y)):
    for index_column, (column_x, column_y) in enumerate(zip(row_x, row_y)):
        mse_value = Find_MSE(per=column_x, sft=column_y)
        #print ("Index_Row = {}".format(index_row))
        #print ("Index_Col = {}".format(index_column))
        Z[index_row][index_column] = mse_value

# Make pd.dataframe from multilayered list:
df = pd.DataFrame(Z,
                  index=list(np.linspace(12.0, 24.0, 121)),
                  columns=list(np.linspace(6.0, 42.0, 361)))
print (df)
print (df.shape)

fig = go.Figure(data=[go.Surface(x=list(np.linspace(6.0, 42.0, 361)),
                                 y=list(np.linspace(12.0, 24.0, 121)),
                                 z=df, opacity=0.8)])

fig.update_layout(scene = dict(xaxis = dict(nticks=7, range=[6.0, 42.0]),
                               yaxis = dict(nticks=7, range=[12.0, 24.0]),
                                xaxis_title='X-axis: PERIOD [6.0-42.0]\n0.5 increments',
                                yaxis_title='Y-axis: SHIFT_V [12.0-24.0]\n0.5 increments',
                                zaxis_title='Z-axis: MSE sum for ~420\n2-gen families'),
                  title='Locked Amplitude = {}'.format(amplitude),
                  autosize=False,
                  width=700, height=700,
                  margin=dict(l=65, r=50, b=65, t=90))

fig.show()
