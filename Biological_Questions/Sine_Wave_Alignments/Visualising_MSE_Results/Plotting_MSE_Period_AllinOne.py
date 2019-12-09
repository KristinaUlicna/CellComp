# TODO: Plot the periods in plotly. Hopefully this is quick...

import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

def Plot3DPeriodDependence_AllinOne():
    directory = '/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE_DataFrame_CSV_Files/'

    fig = go.Figure()

    #for csv in sorted(os.listdir(directory)):           # sorted alphabetically, not numerically!
    for csv in ["MSE_DF_Period_19.0.csv"]:              # if calling specific files is needed!

        dataframe = pd.read_csv(filepath_or_buffer=directory + csv, index_col=[0])

        fig.add_trace(go.Surface(x=[float(item) for item in list(dataframe.columns.values)],
                                 y=[float(item) for item in list(dataframe.index.values)],
                                 z=dataframe.values, opacity=0.8))

    fig.update_traces(contours_z=dict(start=0, end=18000, size=500,
                                      show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))

    fig.update_layout(scene=dict(xaxis = dict(nticks=6, range=[2.0, 12.0]),
                                 yaxis = dict(nticks=7, range=[12.0, 24.0]),
                            xaxis_title='X-axis: Amplitude',
                            yaxis_title='Y-axis: Shift_ver',
                            zaxis_title='Z-axis: MSE 2-gen Families'),
                      title="MSE Dependence on Sine Wave Parameters: Amp, Per, Sft",
                      autosize=False, width=800, height=800, margin=dict(l=65, r=50, b=65, t=90))
    fig.show()


Plot3DPeriodDependence_AllinOne()
