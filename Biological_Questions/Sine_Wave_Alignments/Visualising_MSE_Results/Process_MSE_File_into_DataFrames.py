# Script to split the MSE values line by period & write into separate files as pandas dataframe:

import pandas as pd
import numpy as np

mse_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE_Grid_Search_Shortened.txt"

params = []
for amp in np.linspace(2.0, 12.0, 21):
    for per in np.linspace(6.0, 42.0, 73):
        for shift_v in np.linspace(12.0, 24.0, 25):
            params.append([amp, per, shift_v])

print ("Combos: {}".format(len(params)))

results = []
for i, line in enumerate(open(mse_file, "r")):
    line = line.rstrip()
    if i == 8:                      # MSEs written in line #9!
        line = line.split("\t")
        results = [float(item) for item in line]

print ("MSEs: {}".format(len(results)))

# Make sure the lengths of the params & actual results are the same:
if not len(params) == len(results):
    raise ValueError("There is an MSE value missing for certain params combo")


# Create a list of all perios iterated through to sort data accordingly:
period_list = list(np.linspace(6.0, 42.0, 73))
period_data = [[] for _ in range(len(period_list))]

for item, mse in zip(params, results):
    index = period_list.index(item[1])
    period_data[index].append(mse)


# Process as follows:
for per, period in zip(period_list, period_data):

    # Break all data for one period into 21 lists (each for amplitude) of length equal to 25 (each for shift_v):
    amp_lists = [[] for _ in range(21)]
    index = 0
    counter = 0
    while counter < len(period):
        amp_lists[index] = period[counter:counter+25]
        index += 1
        counter += 25

    # Create the dataframe with rows = shift_v & columns = amplitude and append by columns:
    column_header = 2.0
    df = None
    for order, amp_list in enumerate(amp_lists):
        if order == 0:
            df = pd.DataFrame(data=amp_list,
                              index=np.linspace(12.0, 24.0, 25),
                              columns=np.linspace(column_header, column_header, 1))
        else:
            df.insert(loc=order,
                      column=column_header,
                      value=amp_list)
        column_header += 0.5

    df.name = 'Period_{}'.format(per)
    print(df.name)
    print (df)

    path_to_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/Sine_Wave/Grid_Search/2_gen/MSE_DataFrame_CSV_Files/" \
                   "MSE_DF_{}.csv".format(df.name)
    df.to_csv(path_or_buf=path_to_file)
