#TODO: How to get the number of frames the movie was taken for?
#TODO: How to get the maximum label of cell_ID that were given to the cells? -> so that I don't have to iterate forever...

from lineage import *
call = LineageTree.from_xml("/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml")
trees = call.create()

for order, tree in enumerate(trees):
    if order < 100:
        print (order, tree.track.length, tree.track.z, tree.track.n, tree.track.label, tree.track.fate, end='\n')

# n = [frame, frame, frame, frame, frame, frame, frame, ...]
# label = ['interphase', 'interphase', 'interphase', ...]
# fate = number         TODO: what does this number mean?

def FindMaxFrame(frame):
    max_frame = frame
    counter = 0
    for order, tree in enumerate(trees):
        if order < 100:
            if tree.track.get_copy_at_frame(frame=frame) is not None:
                counter += 1
            if order + 1 == len(trees) and counter == 0:
                max_frame -= 1
                FindMaxFrame(frame = max_frame)
    return max_frame

frame = FindMaxFrame(1200)
print (frame)
frame = FindMaxFrame(1190)
print (frame)
frame = FindMaxFrame(1189)
print (frame)
frame = FindMaxFrame(1188)
print (frame)
frame = FindMaxFrame(1187)
print (frame)
frame = FindMaxFrame(1186)
print (frame)

