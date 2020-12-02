"""
This file is where my general functions are stored
"""

# imported from standard library

# imported from third party repos

# imported from local directories
import config as cfg
import databaseFunctions as dbfunc

# this function takes in a function, runs it, prints to screen the result, and appends the result to a list.
# it is for reducing the repeats on the scrape.py loop
# args = (the list to append to, the function to run, the positional arguments of input func)
def from_func_2_db(my_list, function, *args):
    data = function(*args)
    print(data)
    my_list.append(data)

# above but without the print function
def from_func_2_db_clean(my_list, function, *args):
    data = function(*args)
    my_list.append(data)
    # TODO: should this be decorator?

if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
