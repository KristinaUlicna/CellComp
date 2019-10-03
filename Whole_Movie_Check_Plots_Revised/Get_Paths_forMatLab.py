from Whole_Movie_Check_Plots.Server_Movies_Paths import GetMovieFilesPaths

xml_file_list, _ = GetMovieFilesPaths(exp_type="MDCK_WT_Pure")

mat_file_list = []
for xml_file in xml_file_list:
    mat_file = xml_file.replace("xml", "mat")
    print (mat_file)
    mat_file_list.append(mat_file)

print ("Mat File List: len = {}; {}".format(len(mat_file_list), mat_file_list))