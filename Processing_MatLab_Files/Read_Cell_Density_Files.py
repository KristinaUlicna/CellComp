import scipy.io
mat = scipy.io.loadmat("/Users/kristinaulicna/Documents/Rotation_2/17_07_24-pos6/local_density.mat")
# file analysed: 'pos8_170731'

print (type(mat))       # it's a dictionary!

for keys, values in mat.items():
    print (keys, values)
