from Miscellaneous_Tools.Tracker_Config_Writer.Write_Config_String import CreateTrackerConfig

counter = 25
for max_lost in [1, 2, 3, 4, 5]:
    for prob_not_assign in [1, 0.1, 0.001, 0.0001, 0.00001]:
        print (counter)
        call = CreateTrackerConfig(try_number=counter)
        call.WriteConfigFile(prob_not_assign=prob_not_assign, max_lost=max_lost)
        counter += 1