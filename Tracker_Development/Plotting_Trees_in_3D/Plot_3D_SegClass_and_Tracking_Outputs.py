# TODO: Plot the output of segmentation (HDF data) and tracking (XML data) on top of each other with overlapping colors:

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.io import loadmat
from Local_Cell_Density_Project.SegClass_HDF_Output_Files.HDF_Format_New.HDF5_Data_Functions \
    import GetXandYcoordsPerMovie

# Example plotly scatter plot:
"""
iris = px.data.iris()

print (iris)
print (len(iris))
print (type(iris))
print (list(iris.index.values))
print (list(iris.columns.values))

fig = px.scatter_3d(data=iris,
                    x='sepal_length',
                    y='sepal_width',
                    z='petal_width',
                    color='species')
fig.show()
"""

# Real example:
directory = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
            "tracker_performance_evaluation/tracks_try_55/tracks/"
file_mat = "tracks_type2.mat"
file_txt = "tracks_type2.txt"

# Process the .mat file into a dataframe
mat = loadmat(directory + file_mat)
tracks = mat["tracks"]
df = pd.DataFrame(data=tracks, columns=['x', 'y', 'frame', 'cell_ID', 'parent_ID', 'root_ID', 'class_label'])

print (df)

# Plot the dataframe:

#fig = px.scatter_3d(data_frame=df, x='x', y='y', z='frame',
#                    marker=dict(size=12, color=z, colorscale='Viridis', opacity=0.8))
"""
fig = go.Figure(data=[go.Scatter3d(
    x=df['x'], y=df['y'], z=df['frame'], mode='markers',
    marker=dict(size=3, colorscale='Viridis', opacity=0.5))])

# tight layout
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.show()
"""
"""
# Get the coordinates of HDF file (old format):
hdf5_file = "/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos13/" \
            "tracker_performance_evaluation/tracks_try_55/HDF/segmented.hdf5"
_, _, x_rfp, y_rfp = GetXandYcoordsPerMovie(hdf5_file=hdf5_file)

print (x_rfp)
print (y_rfp)
"""
