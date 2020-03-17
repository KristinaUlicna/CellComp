# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
# ----- POST-PROCESSING OF HDF FILES: APPENDING DATA OF ----- #
#       LOCAL CELL DENSITY, NUCLEUS SIZE & DNA CONTENT        #
#       FROM FLUORESCENCE SIGNAL INTENSITY                    #
#                                                             #
# ----- Creator:            Kristina ULICNA             ----- #
#                                                             #
# ----- Last updated:       31th Jan 2020               ----- #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import os
import sys
import h5py
import math
import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt

from scipy.ndimage import label, find_objects
from tqdm import tqdm
from skimage import io
from PIL import Image

sys.path.append("../")
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths


class Local_Density_Nucleus_Size_Fluo_Signal(object):

    def __init__(self, hdf5_file):
        """ Open & read data from chosen HDF5 file. TODO: This class only processes GFP cells. Deal with it!
            :param hdf5_file (str):                 absolute directory to file: .../HDF/segmented.hdf5
        """

        self.hdf5_file = hdf5_file
        self.hdf5_file_to_read = h5py.File(hdf5_file, 'r')
        self.movie_length = len(self.hdf5_file_to_read["objects"]["obj_type_1"]["map"])
        self.channels = len(list(self.hdf5_file_to_read.values())[0])

        GFP_length = len(self.hdf5_file_to_read["objects"]["obj_type_1"]["coords"])

        if "obj_type_1" not in list(self.hdf5_file_to_read["objects"]):
            raise ValueError("GFP channel not detected in the HDF5 file.")

        self.position = hdf5_file.split("/pos")[1].split("/")[0]
        self.data_date = hdf5_file.split("/pos{}".format(self.position))[0][-6:]
        self.exp_type = "MDCK_WT_Pure"

        if "AB0327" in hdf5_file:
            if "pos0" or "pos2" or "pos4" or "pos6" or "pos8" or "pos10" in hdf5_file:
                self.exp_type = "MDCK_90WT_10Sc_NoComp"

        if "AB0724" in hdf5_file:
            if "pos0" or "pos2" or "pos4" or "pos9" or "pos11" or "pos13" in hdf5_file:
                self.exp_type = "MDCK_90WT_10Sc_NoComp"

        # Initialise the movie if processing fluo_intensity:
        if self.data_date.startswith("AB"):
            raw_movie = "/Volumes/lowegrp/Data/Kristina/{}/17_{}_{}/pos{}/GFP_pos{}.tif" \
                .format(self.exp_type, self.data_date[2:4], self.data_date[4:6], self.position, self.position)
            self.raw_movie = io.imread(raw_movie)

        # Vectors to return:
        self.density = [0 for _ in range(GFP_length)]
        self.nucleus = [0 for _ in range(GFP_length)]
        self.fsignal = [0 for _ in range(GFP_length)]

        #print (len(self.density))
        #print (len(self.nucleus))
        #print (len(self.fsignal))



    def Extract_Cell_Coords(self, frame):
        """ Extract the GFP and RFP cell coordinates, remembering the indexes of these cells.

        :param      frame           (int)
        :return:    cell_coords     (numpy.ndarray)     [[x_coord, y_coord] [x_coord, y_coord] ... ]
                    cell_map        (numpy.ndarray)     [[0 88] [0 20]] -> indices of GFP & RFP cells per frame
        """

        cell_coords = []
        cell_map = []

        for channel in range(1, self.channels + 1):
            map = self.hdf5_file_to_read["objects"]["obj_type_{}".format(channel)]["map"][frame]
            cell_map.append(map)
            for cell in range(map[0], map[1]):
                cell_data = self.hdf5_file_to_read["objects"]["obj_type_{}".format(channel)]["coords"][cell]
                cell_coords.append([cell_data[1], cell_data[2]])
        return np.array(cell_coords), np.array(cell_map)


    def Return_Partial_Density(self, a, b, c):
        """ Construct the triangle given the 'x' & 'y' coordinates of the nuclei centroids.
            1.) Calculate the lengths of the edges of the triangle.
            2.) Compute the approximate area of the whole cell.
            3.) Return a cell density, i.e. an inverse of the cell area.

            :param      a, b, c (lists) ->  [x_coord, y_coord] where 'x_coord' & 'y_coord' are (float)
            :return     partial_density (float) ->  density of the triangle contributing to the cell's area
        """

        a_edge = np.sqrt((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2)
        b_edge = np.sqrt((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2)
        c_edge = np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        s = (a_edge + b_edge + c_edge) / 2
        partial_area = np.sqrt(s * (s - a_edge) * (s - b_edge) * (s - c_edge))

        if partial_area == "nan" or partial_area <= 0:
            return 0.0
        else:
            return 1 / partial_area


    def Calculate_Local_Density(self, frame, show=False):
        """ """

        # 1.) Extract the coordinates of all GFP & RFP cells at specified frame:
        cell_coords, cell_map = self.Extract_Cell_Coords(frame=frame)

        # Take care of blank frames:
        if len(cell_coords) < 3:       # a triangle cannot be created
            return [0.0 for _ in range(len(cell_coords))]

        # 2.) Use the coordinates to construct the Delaunay triangulation of all GFP & RFP cells:
        tri = sp.Delaunay(cell_coords)
        if show is True:
            _ = sp.delaunay_plot_2d(tri=tri)
            plt.xlim(0, 1200)
            plt.ylim(0, 1600)
            plt.title("Delaunay Triangulation for Local Density Calculations")
            plt.xlabel("FiJi Y-axis (pixels)")
            plt.ylabel("FiJi X-axis (pixels)")
            plt.show()
            plt.close()

        # 3.) Create an array of the length of points:
        densities = [0 for _ in range(len(tri.points))]

        # 4.) Calculate the density of each triangle & add to vertex:
        for vertex_index, vertex_coords in zip(tri.simplices, cell_coords[tri.simplices]):
            density = self.Return_Partial_Density(a=vertex_coords[0], b=vertex_coords[1], c=vertex_coords[2])
            for index in vertex_index:
                densities[index] += density

        # Return an intermediate so you can check if correctly calculated:
        breaking_point = cell_map[0][1] - cell_map[0][0]
        self.density[cell_map[0][0]:cell_map[0][1]] = np.array(densities[:breaking_point], dtype=np.float32)
        return densities


    # ---------------------------------------------------------------------------------------------------

    def Calculate_Nuclei_Sizes(self, frame, show=False):
        """ Process the respective binary mask (U-Net output with segmented labels)
            to extract the pixel values of the image into 2D matrix to return.

            1.) Import the 'segmentation' binary mask image & label the pixel values of individual objects.
            2.) Allocate the nuclei centroids from HDF file to each uniquely labelled blob in the binary mask.
            3.) Count the occurence of the label in the processed binary mask & store it's row & column indices.
            4.) Access the corresponding pixels in the raw fluorescence image to calculate average signal intensity.
        """

        cell_coords, cell_map = self.Extract_Cell_Coords(frame=frame)
        pixels = self.hdf5_file_to_read["segmentation"]["images"][frame]

        # Enumerate different objects in the map with unique label & find those objects in the image:
        object_labels, num_features = label(input=pixels)
        found_objects = find_objects(object_labels)

        if num_features != len(found_objects):
            raise ValueError("Warning, number of labelled objects & the objects found with unique label are not equal!")

        # Visualise the binary map & labelled map:
        if show is True:
            plt.imshow(X=pixels)  # plots a 2D array straight ahead!
            plt.title("Raw Segmented Binary Mask at frame #{}".format(frame))
            plt.show()
            plt.close()

            plt.imshow(X=object_labels)  # plots a 2D array straight ahead!
            plt.title("Labelled Segmented Binary Mask at frame #{}".format(frame))
            plt.show()
            plt.close()

        # Match coords to its unique label & sum the appearance of the label in the slice:
        nuclei_size = []
        for coords in cell_coords:
            x, y = int(math.floor(coords[0])), int(math.floor(coords[1]))
            pixel_label = object_labels[x][y]
            image_slice = object_labels[found_objects[pixel_label - 1]]
            nucleus_size = sum([list(row).count(pixel_label) for row in image_slice])
            nuclei_size.append(nucleus_size)

        # Append these sizes into the final array:
        breaking_point = cell_map[0][1] - cell_map[0][0]
        self.nucleus[cell_map[0][0]:cell_map[0][1]] = np.array(nuclei_size[:breaking_point], dtype=np.float32)
        return nuclei_size, object_labels, found_objects


    # ---------------------------------------------------------------------------------------------------

    def Calculate_Fluo_Intensity(self, frame, show=False):
        """ Calculate the average fluorescence intensity of the nucleus based on the pixel value readouts
            from areas superimposed by uniquely labelled binary mask areas by summing them up & averaging.

            :param! raw_images  (str)   ->      absolute directory to folder:

                    Anna's movies:      e.g./Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/17_07_31/pos8/...
                                            which contains STACK TIFFs: 'BF_pos8.tif', 'GFP_pos8.tif', 'RFP_pos8.tif'
                    Giulia's movies:    e.g./Volumes/lowegrp/Data/Guilia/GV0800/pos0/Pos0_aligned/
                                            which contains original BF, GFP & RFP images: e.g.
                                            'img_channel001_position013_time000001104_z000.tif'
        """

        cell_coords, cell_map = self.Extract_Cell_Coords(frame=frame)
        nuclei_size, object_labels, found_objects = self.Calculate_Nuclei_Sizes(frame=frame)
        fluo_signal_intensity_sum = [0 for _ in range(len(nuclei_size))]

        # Initialise the raw images for Anna's & Giulia's movies:
        if self.data_date.startswith("AB"):
            raw_image = self.raw_movie[frame]

        else:
            if self.data_date.startswith("GV"):
                raw_image = "/Volumes/lowegrp/Data/Giulia/{}/pos{}/Pos{}_aligned/img_channel001_position{}_time00000{}_z000.tif" \
                             .format(self.data_date, self.position, self.position, self.position.zfill(3), str(frame).zfill(4))
                if not os.path.isfile(raw_image):
                    return np.array(fluo_signal_intensity_sum, dtype=np.float64)

            if self.data_date.startswith("KU"):
                raw_image = "/Volumes/lowegrp/Data/Kristina/Cells_HeLa/{}/Pos{}/img_channel001_position{}_time00000{}_z000.tif" \
                             .format(self.data_date, self.position, self.position.zfill(3), str(frame).zfill(4))
                if not os.path.isfile(raw_image):
                    return np.array(fluo_signal_intensity_sum, dtype=np.float64)

            # Process the full-sized image (1739 x 1379 pixels):
            image = Image.open(raw_image).convert('L')        # converts the image to 8-bit grayscale
            img_w, img_h = image.size                         # stores image dimensions:
            new_w, new_h = 1600, 1200

            # Define center & crop image accordingly... TODO: Python & FiJi have different offsets!
            if img_w != new_w or img_h != new_h:
                left = (img_w - 1 - new_w) / 2
                top = (img_h - 1 - new_h) / 2
                right = (img_w - 1 + new_w) / 2
                bottom = (img_h - 1 + new_h) / 2
                raw_image = np.array(image.crop((left, top, right, bottom)))  # convert 'PIL.Image.Image' to 'numpy.ndarray'

        # Superimpose the segmented masks with unique labels to the raw fluorescence readout images:
        if len(cell_coords) != len(nuclei_size):
            raise ValueError("Not every cell nucleus had had it's size calculated.")

        for enum, (coords, size) in enumerate(zip(cell_coords, nuclei_size)):
            if size == 0:
                fluo_signal_intensity_sum[enum] = 0.0
            else:
                x, y = int(math.floor(coords[0])), int(math.floor(coords[1]))
                pixel_label = object_labels[x][y]
                found_loc = found_objects[pixel_label - 1]
                image_slice_mask = object_labels[found_loc]
                image_slice_fluo = raw_image[found_loc]

                # This script calculates the sum of the signal intensity per whole nucleus:
                for row_mask, row_fluo in zip(image_slice_mask, image_slice_fluo):
                    for label_pixel, raw_pixel in zip(row_mask, row_fluo):
                        if label_pixel == pixel_label:
                            fluo_signal_intensity_sum[enum] += raw_pixel

        # Append to the final array:
        breaking_point = cell_map[0][1] - cell_map[0][0]
        fluo_signal_intensity_sum = np.array(fluo_signal_intensity_sum[:breaking_point], dtype=np.float32)
        self.fsignal[cell_map[0][0]:cell_map[0][1]] = fluo_signal_intensity_sum
        return fluo_signal_intensity_sum


    # ---------------------------------------------------------------------------------------------------

    def Process_Whole_Movie(self, local_density=False, nucleus_size=False, fluo_signal=False):
        """ """

        for frame in tqdm(range(0, self.movie_length)):
        #for frame in tqdm(range(0, 10)):

            #if frame % 100 == 0:
            #    print("\nCalculating for frame #{} out of {} frames...".format(frame, self.movie_length))

            if local_density is True:
                self.Calculate_Local_Density(frame=frame)
            if nucleus_size is True:
                self.Calculate_Nuclei_Sizes(frame=frame)
            if fluo_signal is True:
                self.Calculate_Fluo_Intensity(frame=frame)

        if self.hdf5_file_to_read.__bool__():
            self.hdf5_file_to_read.close()

        #print (len(self.density))
        #print (len(self.nucleus))
        #print (len(self.fsignal))

        return self.density, self.nucleus, self.fsignal


    def Append_To_HDF(self, local_density=False, nucleus_size=False, fluo_signal=False):

        self.Process_Whole_Movie(local_density=local_density, nucleus_size=nucleus_size, fluo_signal=fluo_signal)

        with h5py.File(self.hdf5_file, 'a') as f:

            if local_density is True:
                if "local_density" in list(f["objects"]["obj_type_1"]):
                    del f["objects"]["obj_type_1"]["local_density"]
                grp_d = f["objects"]["obj_type_1"]
                grp_d.create_dataset(name="local_density", data=self.density)

            if nucleus_size is True:
                if "nucleus_size" in list(f["objects"]["obj_type_1"]):
                    del f["objects"]["obj_type_1"]["nucleus_size"]
                grp_n = f["objects"]["obj_type_1"]
                grp_n.create_dataset(name="nucleus_size", data=self.nucleus)

            if fluo_signal is True:
                if "fluo_signal_sum" in list(f["objects"]["obj_type_1"]):
                    del f["objects"]["obj_type_1"]["fluo_signal_sum"]
                grp_f = f["objects"]["obj_type_1"]
                grp_f.create_dataset(name="fluo_signal_sum", data=self.fsignal)


    def __exit__(self):
        self.hdf5_file_to_read.close()




# Call the class:
movies = Get_MDCK_Movies_Paths()

for movie in movies:
    if "AB0327" in movie:
        if "pos2" in movie or "pos4" in movie or "pos6" in movie or "pos8" in movie or "pos10" in movie:
            hdf5_file = movie + "HDF/segmented.hdf5"
            print ("Calculating for {}".format(hdf5_file))
            Local_Density_Nucleus_Size_Fluo_Signal(hdf5_file=hdf5_file).Append_To_HDF(local_density=True,
                                                                                      nucleus_size=True,
                                                                                      fluo_signal=True)
    if "AB0724" in movie:
        if "pos0" in movie or "pos2" in movie or "pos4" in movie or "pos9" in movie or "pos11" in movie or "pos13" in movie:
            hdf5_file = movie + "HDF/segmented.hdf5"
            print("Calculating for {}".format(hdf5_file))
            Local_Density_Nucleus_Size_Fluo_Signal(hdf5_file=hdf5_file).Append_To_HDF(local_density=True,
                                                                                      nucleus_size=True,
                                                                                      fluo_signal=True)
