import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from PostProcessing_HDF_Data.Local_Density_Nucleus_Size_Fluo_Signal_Create_Class import Local_Density_Nucleus_Size_Fluo_Signal

filename = "/Volumes/lowegrp/Data/Kristina/Cells_MDCK/GV0800/pos0/HDF/segmented.hdf5"
hdf5_file = h5py.File(filename, 'r')

cell_ID =  690
lbepr = hdf5_file["tracks"]["obj_type_1"]["LBEPRChChGen"]
tracks = hdf5_file["tracks"]["obj_type_1"]["tracks"]
map_trk = hdf5_file["tracks"]["obj_type_1"]["map"]
density = hdf5_file["objects"]["obj_type_1"]["density"]
coords = hdf5_file["objects"]["obj_type_1"]["coords"]
labels = hdf5_file["objects"]["obj_type_1"]["labels"]


data = []
coord = []
label = []
st = 0
en = 0
for enum, cells in enumerate(lbepr):
    if cells[0] == cell_ID:
        print (cells)
        st = cells[1]
        en = cells[2]
        map = map_trk[enum]
        for trk in tracks[map[0]:map[1]]:
            data.append(density[trk])
            coord.append(coords[trk])
            label.append(labels[trk])

# TODO: End frame - start frame + 1!!! It's always +1!
print (len(data), data[0:10])
print (len(coord), coord[0:10])
print (len(label), label[0:10])


# Process the data:
den = np.array(data).T.tolist()
raw_den, raw_nuc, raw_sig_avg = den[0], den[2], den[4]
#raw_sig_tot = np.multiply(raw_sig_avg, raw_nuc)
raw_sig_tot = [a*b for a, b in zip(raw_sig_avg, raw_nuc)]


print (raw_den)
print (raw_nuc)
print (raw_sig_avg)
print (raw_sig_tot)

hdf5_file = np.array(coord).T.tolist()[0]
x = np.array(coord).T.tolist()[1]
y = np.array(coord).T.tolist()[2]
l = np.array(label).T.tolist()[0]

frame, raw_den_int, raw_nuc_int, raw_sig_avg_int, raw_sig_tot_int = [], [], [], [], []
for lab, frm, d, n, s1, s2 in zip(l, hdf5_file, raw_den, raw_nuc, raw_sig_avg, raw_sig_tot):
    if lab == 0.0:
        frame.append(frm)
        raw_den_int.append(d)
        raw_nuc_int.append(n)
        raw_sig_avg_int.append(s1)
        raw_sig_tot_int.append(s2)


# Plot the raw & smooth data:

    # Density:
#s1 = UnivariateSpline(x=frame, y=raw_den_int, s=1, ext="extrapolate")
plt.plot(raw_den_int, color="dodgerblue", linewidth=3)
plt.fill_between(x=list(range(len(raw_den_int))), y1=0.0025, y2=raw_den_int, alpha=0.3, color="dodgerblue")
#plt.plot(frame, s1(frame), label="Smooth Data, Interphase")
plt.title("Density -> Cell_ID: {}".format(cell_ID))
plt.savefig("/Users/kristinaulicna/Documents/density.png", bbox_inches="tight")
plt.show()
plt.close()

    # Nucleus:
#s2 = UnivariateSpline(x=frame, y=raw_nuc_int, s=1, ext="extrapolate")
plt.plot(raw_nuc_int, color="forestgreen", linewidth=3)
plt.fill_between(x=list(range(len(raw_nuc_int))), y1=300, y2=raw_nuc_int, alpha=0.3, color="forestgreen")
#plt.plot(frame, s2(frame), label="Smooth Data, Interphase")
plt.title("Nucleus -> Cell_ID: {}".format(cell_ID))
plt.savefig("/Users/kristinaulicna/Documents/nucleus.png", bbox_inches="tight")
plt.show()
plt.close()

    # Fsignal:
#s2 = UnivariateSpline(x=frame, y=raw_sig_avg_int, s=1, ext="extrapolate")
#plt.plot(list(range(st, en + 1)), raw_sig_avg, label="Avg Signal Raw, All States")
#s3 = UnivariateSpline(x=frame, y=raw_sig_tot_int, s=1, ext="extrapolate")
#plt.plot(list(range(st, en + 1)), raw_sig_tot, label="Tot Signal Raw, All States")
#plt.plot(frame, s2(frame), label="Smooth Data Avg, Interphase")
#plt.plot(frame, s3(frame), label="Smooth Data Tot, Interphase")

processed_sig = []
processed_frm = []
for enum, (i, j) in enumerate(zip(raw_sig_tot_int, frame)):
    if i >= 30000:
        processed_sig.append(i)
        processed_frm.append(j)

plt.plot(processed_frm, processed_sig, color="orange", linewidth=3)
plt.fill_between(x=processed_frm, y1=30000, y2=processed_sig, alpha=0.3, color="orange")
#plt.plot(processed_frm, s4(processed_frm), label="Smooth")
plt.title("Fsignal -> Cell_ID: {}".format(cell_ID))
plt.savefig("/Users/kristinaulicna/Documents/fluosig.png", bbox_inches="tight")
plt.show()
plt.close()


def Displacement(x1, y1, x2, y2):
    return np.sqrt( ( (x1-x2) ** 2 ) + ( ( y1-y2 ) ** 2) )

print (x)
print (len(x))
print (y)
print (len(y))

migration = []
for enum, (_, _) in enumerate(zip(x[:], y[:])):
    if enum + 1 < len(x):
        value = Displacement(x1=x[enum], x2=x[enum+1], y1=y[enum], y2=y[enum+1])
        migration.append(value)

plt.plot(migration, color="firebrick", linewidth=3)
plt.fill_between(x=list(range(len(migration))), y1=-0.5, y2=migration, alpha=0.3, color="firebrick")
#plt.plot(processed_frm, s4(processed_frm), label="Smooth")
plt.title("Migration from previous frame -> Cell_ID: {}".format(cell_ID))
plt.savefig("/Users/kristinaulicna/Documents/migration_next.png", bbox_inches="tight")
plt.show()
plt.close()


overall = []
for enum, (_, _) in enumerate(zip(x[:], y[:])):
    if enum != 0:
        value = Displacement(x1=x[0], x2=x[enum], y1=y[0], y2=y[enum])
        overall.append(value)

plt.plot(overall, color="purple", linewidth=3)
plt.fill_between(x=list(range(len(overall))), y1=-0.5, y2=overall, alpha=0.3, color="purple")
#plt.plot(processed_frm, s4(processed_frm), label="Smooth")
plt.title("Migration from initial frame -> Cell_ID: {}".format(cell_ID))
plt.savefig("/Users/kristinaulicna/Documents/migration_start.png", bbox_inches="tight")
plt.show()
plt.close()



    # Neighbours:

distance_100 = [0 for _ in range(st, en + 1)]
distance_200 = [0 for _ in range(st, en + 1)]
distance_300 = [0 for _ in range(st, en + 1)]

call = Local_Density_Nucleus_Size_Fluo_Signal(hdf5_file=filename)

for enum, frejm in enumerate(range(st, en + 1)):
    your_cell = [x[enum], y[enum]]
    cell_coords = call.Extract_Cell_Coords(frame=frejm)
    for c in cell_coords:
        dist = Displacement(x1=your_cell[0], y1=your_cell[1], x2=c[0], y2=c[1])
        if dist <= 100.0:
            distance_100[enum] += 1
        if dist <= 200.0:
            distance_200[enum] += 1
        if dist <= 300.0:
            distance_300[enum] += 1


plt.plot(distance_300, color="darkslateblue", linewidth=2, zorder=0)
plt.fill_between(x=list(range(len(distance_300))), y1=-0.5, y2=distance_300, alpha=0.3, color="darkslateblue")
plt.plot(distance_200, color="darkslateblue", linewidth=2, zorder=1)
plt.fill_between(x=list(range(len(distance_200))), y1=-0.5, y2=distance_200, alpha=0.3, color="darkslateblue")
plt.plot(distance_100, color="darkslateblue", linewidth=2, zorder=2)
plt.fill_between(x=list(range(len(distance_100))), y1=-0.5, y2=distance_100, alpha=0.3, color="darkslateblue")
plt.title("Neighbours -> Cell_ID: {}".format(cell_ID))
plt.savefig("/Users/kristinaulicna/Documents/neighbours.png", bbox_inches="tight")
plt.show()
plt.close()


#print (len(frame), frame[0:10])
#print (len(coord), coord[0:10])
