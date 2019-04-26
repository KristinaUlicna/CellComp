from CellParentPairs_Class import CellParentPairs

# Don't call the class separately for every data_date...
# Make a list of combinations and call all at the same time:

positions = list(range(9)) + list(range(6, 9))
datadates = 9 * ['17_07_31'] + 3 * ['17_07_24']

for pos, date in zip(positions, datadates):
    call = CellParentPairs(pos = pos, data_date=date)
    call.FindCellParents()
    call.CheckFor2Children()
    call.ProgenyLabelling()
    #break
