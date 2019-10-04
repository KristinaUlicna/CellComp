from Cell_Cycle_Duration.Find_Family_Class import FindFamily
from itertools import chain


def CreateGenerationalFile(merged_file, how_many_gen):
    """ Writes a new file with independent families and their generational relationships.

    Options:
        a) 3-generational families
        b) 2-generational families (parent in gen-1 or in gen-2)
        c) 2-generational families (parent in gen-1 only)

    :param how_many_gen:    How many generations you are interested in analysing (options = 2 or 3)
    :return:                None.
    """

    # Define which file you want to create:
    if how_many_gen == 3:
        header_1 = ["Gen_1", "Gen_1", "Gen_1", "Gen_2", "Gen_2", "Gen_2", "Gen_3", "Gen_3", "Gen_3"]
        header_2 = ["Cell_ID", "CCT", "Gener", "Cell_ID", "CCT", "Gener", "Cell_ID", "CCT", "Gener"]
    elif how_many_gen == 2:
        header_1 = ["Gen_1", "Gen_1", "Gen_1", "Gen_2", "Gen_2", "Gen_2"]
        header_2 = ["Cell_ID", "CCT", "Gener", "Cell_ID", "CCT", "Gener"]
    else:
        raise Exception("Warning, define the number of generations to search for")

    # Write the file & initiate with headers:
    directory = "/".join(merged_file.split("/")[:-1])
    result_file = directory + "/generation_{}_families.txt".format(how_many_gen)
    result_file = open(result_file, "w")

    header_string = ""
    for item in header_1:
        header_string += str(item) + "\t"
    header_string = header_string[:-1] + "\n"
    result_file.write(header_string)

    header_string = ""
    for item in header_2:
        header_string += str(item) + "\t"
    header_string = header_string[:-1] + "\n"
    result_file.write(header_string)

    # Search the file:
    for line in open(merged_file, "r"):
        line = line.rstrip().split("\t")
        if line[0] != "Cell_ID-posX-date":
            string = ""
            info = []
            call = FindFamily(cell_ID=line[0], filtered_file=merged_file)
            if int(line[5]) == how_many_gen:
                cellID_info = call.FindItself()
                parent_info = call.FindParent()
                info = list(chain.from_iterable([parent_info, cellID_info]))
            if how_many_gen == 3:
                grand_info = call.FindGrandparent()
                info = grand_info + info

            # Write the line which fulfills the requirements into the file:
            if len(info) != 0:
                for item in info:
                    string += str(item) + "\t"
                string = string[:-1] + "\n"
                result_file.write(string)

    result_file.close()


# Call the function:
merged_file = "/Volumes/lowegrp/Data/Kristina/MDCK_WT_Pure/cellIDdetails_merged.txt"
CreateGenerationalFile(merged_file=merged_file, how_many_gen=3)
CreateGenerationalFile(merged_file=merged_file, how_many_gen=2)
