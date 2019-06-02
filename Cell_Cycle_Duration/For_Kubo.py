# Lists are 'mutable' array-like iterable:

my_list = ["I", "am", "hungry"]
print (my_list)
print (" ".join(my_list))

# Mutable = specific elements in the lists (in our case, 3 strings)
# can be renamed by numerical indexing:

my_list[0] = "You"
my_list[1] = "were"
print (my_list)
print (" ".join(my_list))

# If you had a tuple, which is pretty much an array of the same structure,
# you wouldn't be able to rename the elements by indexing:

my_tuple = tuple(my_list)
print (my_tuple)



