# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                             #
# ----- POST-PROCESSING OF HDF FILES: APPENDING DATA OF ----- #
#       LOCAL CELL DENSITY, NUCLEUS SIZE & DNA CONTENT        #
#       FROM FLUORESCENCE SIGNAL INTENSITY                    #
#                                                             #
# ----- Class #1:           Local Density Calculations  ----- #
#                                                             #
# ----- Creator:            Kristina ULICNA             ----- #
#                                                             #
# ----- Last updated:       30th Jan 2020               ----- #
#                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import h5py
import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt
from Movie_Analysis_Pipeline.Single_Movie_Processing.Server_Movies_Paths import Get_MDCK_Movies_Paths


class Local_Density(object):

    def __init__(self, hdf5_file):
        """ Open & read data from HDF5 file.
        :param hdf5_file (str): absolute directory to file: /segmented.hdf5
        """

        self.hdf5_file = hdf5_file
        self.file = h5py.File(hdf5_file, 'r')
        self.movie_length = len(self.file["objects"]["obj_type_1"]["map"])
        print (self.movie_length)
        self.channels = len(list(self.file.values())[0])

        self.density_GFP = [0 for _ in range(len(self.file["objects"]["obj_type_1"]["coords"]))]
        if self.channels > 1:
            self.density_RFP = [0 for _ in range(len(self.file["objects"]["obj_type_2"]["coords"]))]


    def Extract_Cell_Coords(self, frame):
        """ Extract the GFP and RFP cell coordinates, remembering the indexes of these cells.

        :param      frame           (int)
        :return:    cell_coords     (numpy.ndarray)     [[x_coord, y_coord] [x_coord, y_coord] ... ]
                    cell_map        (numpy.ndarray)     [[0 88] [0 20]] -> indices of GFP & RFP cells per frame
        """

        cell_coords = []
        cell_map = []
        for channel in range(1, self.channels + 1):
            map = self.file["objects"]["obj_type_{}".format(channel)]["map"][frame]
            cell_map.append(map)
            for cell in range(map[0], map[1]):
                cell_data = self.file["objects"]["obj_type_{}".format(channel)]["coords"][cell]
                cell_coords.append([cell_data[1], cell_data[2]])
        return np.array(cell_coords), np.array(cell_map)


    def Visualise_Delaunay_Triang(self, tri):
        _ = sp.delaunay_plot_2d(tri=tri)
        plt.xlim(0, 1200)
        plt.ylim(0, 1600)
        plt.title("Delaunay Triangulation for Local Density Calculations")
        plt.xlabel("FiJi Y-axis (pixels)")
        plt.ylabel("FiJi X-axis (pixels)")
        plt.show()
        plt.close()


    def Calculate_Triangle_Density(self, a, b, c):
        """ Input: coordinates of the triangle vertex.

            a = [x_coord, y_coord]
            b = [x_coord, y_coord]
            c = [x_coord, y_coord]
        """

        a_edge = np.sqrt((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2)
        b_edge = np.sqrt((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2)
        c_edge = np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        s = (a_edge + b_edge + c_edge) / 2
        area = np.sqrt(s * (s - a_edge) * (s - b_edge) * (s - c_edge))

        return 1 / area


    def Calculate_for_Movie(self):
        """ """

        for frame in range(0, self.movie_length):

            if frame % 100 == 0:
                print ("Calculating for frame #{}".format(frame))

            # 1.) Extract the coordinates of all GFP & RFP cells at specified frame:
            cell_coords, cell_map = self.Extract_Cell_Coords(frame=frame)

            # 2.) Use the coordinates to construct the Delaunay triangulation of all GFP & RFP cells:
            tri = sp.Delaunay(cell_coords)

            # 3.) Create an array of the length of points:
            densities = [0 for _ in range(len(tri.points))]

            # Calculate the density of each triangle & add to vertex:
            for vertex_index, vertex_coords in zip(tri.simplices, cell_coords[tri.simplices]):
                density = self.Calculate_Triangle_Density(a=vertex_coords[0], b=vertex_coords[1], c=vertex_coords[2])
                for index in vertex_index:
                    densities[index] += density

            # Break the list depending on which cells are GFP and which are RFP:
            breaking_point = cell_map[0][1] - cell_map[0][0]

            # Write these definitive cell densities into the big density array:
            if self.channels == 1:
                self.density_GFP[cell_map[0][0]:cell_map[0][1]] = densities[:breaking_point]
            else:
                self.density_GFP[cell_map[0][0]:cell_map[0][1]] = densities[:breaking_point]
                self.density_RFP[cell_map[1][0]:cell_map[1][1]] = densities[breaking_point:]


        if self.channels == 1:
            return np.array(self.density_GFP, dtype=np.float32)
        else:
            return np.array(self.density_GFP, dtype=np.float32), np.array(self.density_RFP, dtype=np.float32)


    def Append_to_HDF(self):
        """ """

        self.Calculate_for_Movie()
        if self.file.__bool__:
            self.file.close()

        with h5py.File(self.hdf5_file, 'a') as f:
            for channel in range(1, self.channels + 1):
                if "density" in list(f["objects"]["obj_type_{}".format(channel)]):
                    del f["objects"]["obj_type_{}".format(channel)]["density"]

                grp = f["objects"]["obj_type_{}".format(channel)]

                if channel == 1:
                    grp.create_dataset(name="density", data=self.density_GFP)
                elif channel == 2:
                    grp.create_dataset(name="density", data=self.density_RFP)
                else:
                    raise ValueError("Warning, specify the channel (1 = 'GFP', 2 = 'RFP')")




# Call the class:
movies = Get_MDCK_Movies_Paths()

for enum, movie in enumerate(movies):
    print ("Movie {} out of {} -> {}".format(enum, len(movies), movie))
    hdf5_file = movie + "HDF/segmented.hdf5"
    Local_Density(hdf5_file=hdf5_file).Append_to_HDF()
