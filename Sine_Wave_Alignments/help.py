import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 48, 48 * 5 + 1)
y = 4 * np.sin(2*np.pi/24 * x + 0) + 18

plt.plot(x, y, color="dodgerblue", linewidth=3.0)
plt.xticks(list(range(0, 48+1, 6)))
plt.xlabel("Oscillation Period / Time [hours]")
plt.ylabel("Cell Cycle Duration [hours]")
plt.title("Sine Wave: y(x) = 4.0 * sin(2*pi/24.0 * x + 0) + 18.0")
plt.grid(which="both")
plt.show()
plt.close()

top_mse = [1000000 for _ in range(10)]
top_params = [[] for _ in range(10)]

for best_model_mse, mini_list in zip([19, 18, 17, 26, 15, 14, 13, 12, 11, 10, 9, 8, 7, 5, 1], [[1.0, 3.5, 18.9], [2.0, 3.5, 18.9], [3.0, 3.5, 18.9], [1.0, 3.5, 18.9], [2.0, 3.5, 18.9], [3.0, 3.5, 18.9], [1.0, 3.5, 18.9], [2.0, 3.5, 18.9], [3.0, 3.5, 18.9], [1.0, 3.5, 18.9], [2.0, 3.5, 18.9], [3.0, 3.5, 18.9], [1.0, 3.5, 18.9], [2.0, 3.5, 18.9], [3.0, 3.5, 18.9]]):
    if best_model_mse < top_mse[0]:
        for i in range(8, -1, -1):  # reversed order
            top_mse[i + 1] = top_mse[i]
            top_params[i + 1] = top_params[i]
        top_mse[0] = best_model_mse
        top_params[0] = mini_list
    print (top_mse)
    print (top_params)

#top_mse = [10.18, 23.01, 28.80]
#top_params = [[1.0, 3.5, 18.9], [2.0, 3.5, 18.9], [3.0, 3.5, 18.9]]

print ("Top 10 Solutions:\n")
for counter, (mse, params) in enumerate(zip(top_mse, top_params)):
    print ("\tTop #{}:\tMean Squared Error = {}\tParameters = {}".format(counter + 1, mse, params))


# y(x) = 4.6 * sin ( 2*pi / 11.7 * x + 0 ) + 17.7


counter = 0

for amp in np.linspace(4.5, 4.7, 20 + 1):
    for per in np.linspace(11.6, 11.8, 20 + 1):
        for shift_v in np.linspace(17.6, 17.8, 20 + 1):
            counter += 1

print (counter)

# BEFORE: 4411781 (increments = 0.1)    3-gen families
# AFTER:  563091  (increments = 0.2)    2-gen families

print (4.6 % 0.1)

per = 11.7
phase = np.linspace(0, per + 1, int(per * 5))
print (phase)
print (len(phase))

number = 24.6 / 0.2
print (number)

vector = np.linspace(0, 11.7, int(11.7 / 0.2 + 1))

#2 options:
#24.6 or 11.7
print ("HERE!")


"""
>>> np.linspace(0,1,11)
array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ])
>>> np.linspace(0,1,10,endpoint=False)
array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9])
"""
per = 24.6
vector = np.linspace(0, per, int(per*10) + 1)
print (len(vector))
print (vector)

for per in range (6, 42 + 1, 1):
    repeats = int(72.0 / per)
    if repeats <= 1:
        repeats += 1
    print (repeats)
