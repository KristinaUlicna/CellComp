import os
import h5py

def FindMovieLength(exp_type, data_date, pos):
    """ Returns movie_frames (integer) of how long the movie is according to the specified arguments (strings). """

    movie_directory = "/Volumes/lowegrp/Data/Kristina/{}/{}/{}/segmented/".format(exp_type, data_date, pos)
    directory = os.listdir(movie_directory)
    directory = [item for item in sorted(directory) if item.startswith("s_") and item.endswith(".tif")]
    return len(directory)


def FindMovieLengthFromHDF(pos, data_date, exp_type="Cells_MDCK", user="Kristina"):
    """ :param:     directory -> .../user/exp_type/data_date/pos/   """

    directory = "/Volumes/lowegrp/Data/{}/{}/{}/pos{}/HDF/segmented.hdf5".format(user, exp_type, data_date, pos)
    hdf5_file = h5py.File(directory, 'r')
    frame_volume = len(hdf5_file["objects"]["obj_type_1"]["map"])
    return frame_volume
