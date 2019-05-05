#TODO: Create a script which will import Alan's generation tree code - use 'lineage.py' module.

from lineage import *

t = LineageTree.from_xml("/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml")
print (t)
trees = t.create()      # it's a list of Nodes (=classes)
print (trees)
print ("How many nodes in first layer? {}\n".format(len(trees)))

def FindCellByID(cell_ID):
    FOUND = False
    cells_node = None
    generation = None
    for order, gen0_founder in enumerate(trees):
        # Generation 0:
        if gen0_founder.ID == cell_ID:
            FOUND = True
            cells_node = order
            generation = 0
            break
        if gen0_founder.leaf is False:
            gen1_left1 = gen0_founder.children[0]
            gen1_right2 = gen0_founder.children[1]
            # Generation 1:
            if gen1_left1.ID == cell_ID or gen1_right2.ID == cell_ID:
                FOUND = True
                cells_node = order
                generation = 1
                break
            if gen1_left1.leaf is False:
                gen2_left1 = gen1_left1.children[0]
                gen2_right2 = gen1_left1.children[1]
                # Generation 2:
                if gen2_left1.ID == cell_ID or gen2_right2.ID == cell_ID:
                    FOUND = True
                    cells_node = order
                    generation = 2
                    break
                if gen2_left1.leaf is False:
                    gen3_left1 = gen2_left1.children[0]
                    gen3_right2 = gen2_left1.children[1]
                    # Generation 3:
                    if gen3_left1.ID == cell_ID or gen3_right2.ID == cell_ID:
                        FOUND = True
                        cells_node = order
                        generation = 3
                        break
                    if gen3_left1.leaf is False:
                        gen4_left1 = gen3_left1.children[0]
                        gen4_right2 = gen3_left1.children[1]
                        # Generation 4:
                        if gen4_left1.ID == cell_ID or gen4_right2.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break
                    if gen3_right2.leaf is False:
                        gen4_left3 = gen3_right2.children[0]
                        gen4_right4 = gen3_right2.children[1]
                        # Generation 4:
                        if gen4_left3.ID == cell_ID or gen4_right4.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break
                if gen2_right2.leaf is False:
                    gen3_left3 = gen2_right2.children[0]
                    gen3_right4 = gen2_right2.children[1]
                    # Generation 3:
                    if gen3_left3.ID == cell_ID or gen3_right4.ID == cell_ID:
                        FOUND = True
                        cells_node = order
                        generation = 3
                        break
                    if gen3_left3.leaf is False:
                        gen4_left5 = gen3_left3.children[0]
                        gen4_right6 = gen3_left3.children[1]
                        # Generation 4:
                        if gen4_left5.ID == cell_ID or gen4_right6.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break
                    if gen3_right4.leaf is False:
                        gen4_left7 = gen3_right4.children[0]
                        gen4_right8 = gen3_right4.children[1]
                        # Generation 4:
                        if gen4_left7.ID == cell_ID or gen4_right8.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break
            if gen1_right2.leaf is False:
                gen2_left3 = gen1_right2.children[0]
                gen2_right4 = gen1_right2.children[1]
                # Generation 2:
                if gen2_left3.ID == cell_ID or gen2_right4.ID == cell_ID:
                    FOUND = True
                    cells_node = order
                    generation = 2
                    break
                if gen2_left3.leaf is False:
                    gen3_left5 = gen2_left3.children[0]
                    gen3_right6 = gen2_left3.children[1]
                    # Generation 3:
                    if gen3_left5.ID == cell_ID or gen3_right6.ID == cell_ID:
                        FOUND = True
                        cells_node = order
                        generation = 3
                        break
                    if gen3_left5.leaf is False:
                        gen4_left9 = gen3_left5.children[0]
                        gen4_right10 = gen3_left5.children[1]
                        # Generation 4:
                        if gen4_left9.ID == cell_ID or gen4_right10.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break
                    if gen3_right6.leaf is False:
                        gen4_left11 = gen3_right6.children[0]
                        gen4_right12 = gen3_right6.children[1]
                        # Generation 4:
                        if gen4_left11.ID == cell_ID or gen4_right12.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break
                if gen2_right4.leaf is False:
                    gen3_left7 = gen2_right4.children[0]
                    gen3_right8 = gen2_right4.children[1]
                    # Generation 3:
                    if gen3_left7.ID == cell_ID or gen3_right8.ID == cell_ID:
                        FOUND = True
                        cells_node = order
                        generation = 3
                        break
                    if gen3_left7.leaf is False:
                        gen4_left13 = gen3_left7.children[0]
                        gen4_right14 = gen3_left7.children[1]
                        # Generation 4:
                        if gen4_left13.ID == cell_ID or gen4_right14.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break
                    if gen3_right8.leaf is False:
                        gen4_left15 = gen3_right8.children[0]
                        gen4_right16 = gen3_right8.children[1]
                        # Generation 4:
                        if gen4_left15.ID == cell_ID or gen4_right16.ID == cell_ID:
                            FOUND = True
                            cells_node = order
                            generation = 4
                            break

    #TODO: Code works only for four generations! Extend to eight generations, or len(dictionary):
    if FOUND:
        print ("Cell #{}; Node #{}; Generation #{}".format(cell_ID, cells_node, generation))
        if cells_node == None or generation == None:
            print ("Cell #{} doesn't appear in the movie / is not tracked.".format(cell_ID))
    else:
        print ("Cell #{} was not mapped. Sorry!".format(cell_ID))

    return cell_ID, FOUND, cells_node, generation


# Explore Node #8:
FindCellByID(103)
FindCellByID(1961)
FindCellByID(1960)
FindCellByID(7157)
FindCellByID(7158)
FindCellByID(10864)
FindCellByID(10861)
FindCellByID(11322)
FindCellByID(11388)
FindCellByID(12506)
FindCellByID(12504)
FindCellByID(11518)
FindCellByID(11531)
FindCellByID(11582)
FindCellByID(11580)
FindCellByID(12015)
FindCellByID(12016)
print ()

"""
# Explore all cells:
found_list = []
node_list = []
gener_list = []

for cell in range(0, 12000):
    _, found, cells_node, generation = FindCellByID(cell_ID = cell)
    found_list.append(found)
    node_list.append(cells_node)
    gener_list.append(generation)

print (found_list)
print (node_list)
print (gener_list)
print ()


# Get some statistics:
for i in range(0, 5):
    print("Number of cells present in generation #{}: {}".format(i, gener_list.count(i)))
print ("Number of cells not appearing in the movie: {}".format(gener_list.count(None)))

nodes_over2gen = []
for node, gener in zip(node_list, gener_list):
    if gener != None and gener > 2:
        nodes_over2gen.append(node)
nodes_over2gen = sorted(set(nodes_over2gen))
print ("\nWhich nodes cover more than 2 generations? How many in total? {}\t{}".format(len(nodes_over2gen), nodes_over2gen))

for item in nodes_over2gen:
    print("Node #{} with more than 2 generations:\t{}".format(item, trees[item].to_dict()))

#TODO: Max cell label? - to know how long I need to iterate over
#TODO: Access # of cells per tree & number of generations per tree

"""