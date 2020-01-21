# TODO: Plot the periods in plotly. Hopefully this is quick...

import plotly.graph_objects as go
import pandas as pd
import numpy as np

def Plot3DPeriodDependence(period, show=False):
    dataframe = pd.read_csv(filepath_or_buffer='/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/'
                         '2_gen/MSE_DataFrame_CSV_Files/MSE_DF_Period_{}.csv'.format(period), index_col=[0])

    fig = go.Figure(data=[go.Surface(x=[float(item) for item in list(dataframe.columns.values)],
                                     y=[float(item) for item in list(dataframe.index.values)],
                                     z=dataframe.values, opacity=0.8)])

    fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))

    fig.update_layout(scene=dict(xaxis = dict(nticks=6, range=[2.0, 12.0]),
                                 yaxis = dict(nticks=7, range=[12.0, 24.0]),
                            xaxis_title='X-axis: Amplitude',
                            yaxis_title='Y-axis: Shift_ver',
                            zaxis_title='Z-axis: MSE 2-gen Families'),
                      title="MSE Dependence of 'Period' = {} on Sine Wave Parameters".format(period),
                      autosize=False, width=800, height=800, margin=dict(l=65, r=50, b=65, t=90))

    if show is True:
        fig.show()


for value in [19.0]:
    Plot3DPeriodDependence(period=value)
