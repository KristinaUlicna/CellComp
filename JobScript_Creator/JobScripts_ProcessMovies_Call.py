# Call the ProcessMovies class & its functions:
from JobScripts_ProcessMovies_Class import ProcessMovies

# Loop through multiple positions:

for position in range(0, 9):
    call = ProcessMovies(position, data_date='17_07_31')
    #call.SegClass()
    call.Tracking()

for position in range(6, 9):
    call = ProcessMovies(position, data_date='17_07_24')
    #call.SegClass()
    call.Tracking()

for position in [0, 1, 2, 11, 12, 13]:
    call = ProcessMovies(position, data_date='17_07_10')
    #call.SegClass()
    call.Tracking()

for position in range(7, 10):
    call = ProcessMovies(position, data_date='17_01_24')
    #call.SegClass()
    call.Tracking()


# Create jobs for specific position:

#call = ProcessMovies(6, data_date='17_07_24')
#call.SegClass()
#call.Tracking()