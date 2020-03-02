# TODO: Shortlist a cell and see which cells it forms triangles with, send those to Chris:

import h5py
from PostProcessing_HDF_Data.Local_Density_Nucleus_Size_Fluo_Signal_Create_Class import Local_Density_Nucleus_Size_Fluo_Signal

hdf5_file = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos0/HDF_copy/segmented.hdf5"
frame = 862

call = Local_Density_Nucleus_Size_Fluo_Signal(hdf5_file=hdf5_file)
coords = call.Extract_Cell_Coords(frame=frame)      # there should be 313 cells in this frame

cell = 257
cell_coords = coords[cell]                          # [1062.5222   178.20424]
print (cell_coords)

densities = call.Calculate_Local_Density(frame=frame, show=True)
print (densities[cell])
