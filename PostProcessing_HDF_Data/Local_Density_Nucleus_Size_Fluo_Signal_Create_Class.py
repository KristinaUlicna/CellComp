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
import h5py
import math
import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt

from scipy.ndimage import label, find_objects
from tqdm import tqdm
from PIL import Image


class Local_Density_Nucleus_Size_Fluo_Signal(object):

    def __init__(self, hdf5_file):
        """ Open & read data from chosen HDF5 file. TODO: This class only processes GFP cells. Deal with it!
            :param hdf5_file (str):                 absolute directory to file: .../HDF/segmented.hdf5
        """

        self.hdf5_file = h5py.File(hdf5_file, 'r')
        self.movie_length = len(self.hdf5_file["objects"]["obj_type_1"]["map"])
        GFP_length = len(self.hdf5_file["objects"]["obj_type_1"]["coords"])

        if "obj_type_1" not in list(self.hdf5_file["objects"]):
            raise ValueError("GFP channel not detected in the HDF5 file.")

        self.position = hdf5_file.split("/pos")[1].split("/")[0]
        self.data_date = hdf5_file.split("/pos{}".format(self.position))[0][-6:]
        self.cell_map = None

        if not self.data_date.startswith("AB") and not self.data_date.startswith("GV"):
            raise AttributeError("Wrong HDF file initiation on position <{}> or data_date <{}>."
                                 .format(self.position, self.data_date))

        # Vectors to return:
        self.density = [0 for _ in range(GFP_length)]
        self.nucleus = [0 for _ in range(GFP_length)]
        self.fsignal = [0 for _ in range(GFP_length)]


    def Extract_Cell_Coords(self, frame):
        """ Extract the GFP and RFP cell coordinates, remembering the indexes of these cells.

        :param      frame           (int)
        :return:    cell_coords     (numpy.ndarray)     [[x_coord, y_coord] [x_coord, y_coord] ... ]

        """

        self.cell_map = self.hdf5_file["objects"]["obj_type_1"]["map"][frame]
        cell_coords = []
        for cell in range(self.cell_map[0], self.cell_map[1]):
            cell_data = self.hdf5_file["objects"]["obj_type_1"]["coords"][cell]
            cell_coords.append([cell_data[1], cell_data[2]])

        return np.array(cell_coords)


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
        cell_coords = self.Extract_Cell_Coords(frame=frame)

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

        # 5.) Write these definitive cell densities into the big density array:
        self.density[self.cell_map[0]:self.cell_map[1]] = densities

        # 6.) Return an intermediate so you can check if correctly calculated:
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

        cell_coords = self.Extract_Cell_Coords(frame=frame)
        pixels = self.hdf5_file["segmentation"]["images"][frame]

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
        self.nucleus[self.cell_map[0]:self.cell_map[1]] = np.array(nuclei_size, dtype=np.float64)

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

        cell_coords = self.Extract_Cell_Coords(frame=frame)
        nuclei_size, object_labels, found_objects = self.Calculate_Nuclei_Sizes(frame=frame)
        fluo_signal_int = [0 for _ in range(len(nuclei_size))]

        if self.data_date.startswith("AB"):
            return np.array(fluo_signal_int, dtype=np.float64)

        if self.data_date.startswith("GV"):
            img = "/Volumes/lowegrp/Data/Giulia/{}/pos{}/Pos{}_aligned/img_channel001_position{}_time00000{}_z000.tif"\
                   .format(self.data_date, self.position, self.position, self.position.zfill(3), str(frame).zfill(4))

            if os.path.isfile(img):

                # Process the full-sized image:
                image = Image.open(img).convert('L')          # converts the image to 8-bit grayscale
                img_w, img_h = image.size                     # stores image dimensions:
                new_w, new_h = 1600, 1200
                data = np.array(image.getdata())              # converts data to single pixel list; len = 1600 x 1200
                pixels = [data[offset:offset + img_w] for offset in range(0, img_w * img_h, img_w)]
                    # converts data to 2D list (list of 'numpy.ndarray' of 'numpy.int64'); access via pixels[row][col]

                # Define center & crop image accordingly:
                left = (img_w - new_w) / 2
                top = (img_h - new_h) / 2
                right = (img_w + new_w) / 2
                bottom = (img_h + new_h) / 2
                fluo_raw_im = image.crop((left, top, right, bottom))

                # Visualise the image:
                if show is True:
                    plt.imshow(X=pixels)
                    plt.title("Full-sized GFP image ({} x {} pixels) at frame #{}".format(img_w, img_h, frame))
                    plt.show()
                    plt.close()

                if show is True:
                    plt.imshow(X=fluo_raw_im)
                    plt.title("Rescaled GFP image ({} x {} pixels) at frame #{}".format(new_w, new_h, frame))
                    plt.show()
                    plt.close()

                # Check whether the dimensions of your uniquely labelled image & your raw fluo image are the same:
                fluo_raw_im = np.array(fluo_raw_im)     # convert 'PIL.Image.Image' to 'numpy.ndarray'

                if object_labels.shape[0] != fluo_raw_im.shape[0] or object_labels.shape[1] != fluo_raw_im.shape[1]:
                    raise ValueError("Dimensions of uniquely labelled image <{}> & raw fluorescence image <{}> "
                                     "are not matching! -> It should be <{}>".format(object_labels.shape,
                                                                                     fluo_raw_im.shape,
                                                                                     (new_h, new_w)))

                # Superimpose the segmented masks with unique labels to the raw fluorescence readout images:
                if len(cell_coords) != len(nuclei_size):
                    raise ValueError("Not every cell nucleus had had it's size calculated.")

                for enum, (coords, size) in enumerate(zip(cell_coords, nuclei_size)):

                    if size == 0:
                        fluo_signal_int[enum] = 0.0

                    else:
                        x, y = int(math.floor(coords[0])), int(math.floor(coords[1]))
                        pixel_label = object_labels[x][y]
                        found_loc = found_objects[pixel_label - 1]
                        image_slice_mask = object_labels[found_loc]
                        image_slice_fluo = fluo_raw_im[found_loc]

                        fluo_value_sum = 0
                        for row_mask, row_fluo in zip(image_slice_mask, image_slice_fluo):
                            for label_pixel, raw_pixel in zip(row_mask, row_fluo):
                                if label_pixel == pixel_label:
                                    fluo_value_sum += raw_pixel

                        fluo_signal_int[enum] = float(float(fluo_value_sum) / float(size))

                self.fsignal[self.cell_map[0]:self.cell_map[1]] = np.array(fluo_signal_int, dtype=np.float64)
                return np.array(fluo_signal_int, dtype=np.float64)

            else:
                return np.array(fluo_signal_int, dtype=np.float64)


    # ---------------------------------------------------------------------------------------------------

    def Process_Whole_Movie(self, local_density=False, nucleus_size=False, fluo_signal=False):
        """ """

        for frame in tqdm(range(0, self.movie_length)):
        #for frame in tqdm(range(0, 10)):

            if frame % 10 == 0:
                print("\nCalculating for frame #{} out of {} frames...".format(frame, self.movie_length))

            if local_density is True:
                self.Calculate_Local_Density(frame=frame)
            if nucleus_size is True:
                self.Calculate_Nuclei_Sizes(frame=frame)
            if fluo_signal is True:
                self.Calculate_Fluo_Intensity(frame=frame)

        if self.hdf5_file.__bool__():
            self.hdf5_file.close()

        return self.density, self.nucleus, self.fsignal

    # ---------------------------------------------------------------------------------------------------------

    def __exit__(self):
        self.hdf5_file.close()