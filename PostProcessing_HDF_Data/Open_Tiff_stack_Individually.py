# TODO: Open Anna's movies, saved as a single file TIFF, as individual tiff images to read cell nucleus intensities.

from skimage import io

movie_GFP = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos8/GFP_pos8.tif"

im = io.imread(movie_GFP)
print (im.shape)
# (1198, 1200, 1600) corresponds to (z, y, x)

print (im[0].shape)
# (1200, 1600) corresponds to (y, x)