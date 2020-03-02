#TODO: Write functions to calculate spatial & temporal displacement



def displacement_spatial(term, init):

    with open(self.directory + file) as json_file:
        data = json.load(json_file)

        if data['fate'] == "DIVIDE":

            #print ("Divides: {}".format(file))

            x_p = float(data['x'][-1])
            y_p = float(data['y'][-1])
            children = [int(data['children'][0]), int(data['children'][1])]
            frame_div = int(data['t'][-1])
            cell_count = GetCellCountPerFrame(hdf5_file=self.hdf5_file, frame=frame_div)

            x_c = [[] for _ in range(2)]
            y_c = [[] for _ in range(2)]

