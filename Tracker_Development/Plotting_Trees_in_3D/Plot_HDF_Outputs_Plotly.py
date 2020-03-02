import plotly.express as px
from SegClass_HDF_Output_Files.HDF_Format_Old import GetXandYcoordinatesPerFrame

#TODO: Plot the scatter plot of all cells in 3D in Plotly

file = '/Volumes/lowegrp/Data/Kristina/MDCK_90WT_10Sc_NoComp/17_07_24/pos0/HDF/segmented.hdf5'

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for frame in range(0, 1105):
    if frame % 10 == 0:
        print ("Processing frame #{}".format(frame))
    x_gfp, y_gfp, x_rfp, y_rfp = GetXandYcoordinatesPerFrame(hdf5_file=file, frame=frame)
    ax.scatter(x_gfp, y_gfp, frame, s=1, color="forestgreen", label="GFP")
    ax.scatter(x_rfp, y_rfp, frame, s=1, color="magenta", label="RFP")
    break

ax.set_xlabel('X coordinate [pixels]')
ax.set_ylabel('Y coordinate [pixels]')
ax.set_zlabel('Time [frames]')

plt.show()




print (iris)
print (type(iris))

fig = px.scatter_3d()

"""
fig = px.scatter_3d(iris, x='sepal_length', y='sepal_width', z='petal_width', color='species')
fig.show()
"""