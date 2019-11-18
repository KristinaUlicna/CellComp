import os

def FindMovieLength(exp_type, data_date, pos):
    """ Returns movie_frames (integer) of how long the movie is according to the specified arguments (strings). """

    movie_directory = "/Volumes/lowegrp/Data/Kristina/{}/{}/{}/segmented/".format(exp_type, data_date, pos)
    directory = os.listdir(movie_directory)
    directory = [item for item in sorted(directory) if item.startswith("s_") and item.endswith(".tif")]
    return len(directory)