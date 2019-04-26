# Call the ProcessMovies class & its functions:
from JobScripts_ProcessMovies_Class import ProcessMovies

# Loop through multiple positions:
"""
for position in range(0, 9):
    call = ProcessMovies(position, data_date='17_07_31')
    #call.SegClass()
    #call.Tracking()
"""

# Create jobs for specific position:
"""
call = ProcessMovies(6, data_date='17_07_24')
call.SegClass()
call.Tracking()
"""