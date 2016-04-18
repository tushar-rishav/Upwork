# -*- coding: utf-8 -*-

import ast
from os.path import isfile, expanduser

def manageInventory(stockFile: str="stock.json", queueFile: str="queue.json"):
    """
    Run analysis and return the result for managing inventory
    :param stockFile:
        The filepath for Stock File
    :param queueFile:
        The filepath for Queue file
    """
    if not (isfile(expanduser(stockFile)) and isfile(expanduser(queueFile))): 
        raise Exception('The {} file does not exists'.format(portTextFile))
    
    stock = {}
    queue = []
    with open(stockFile, 'r') as sf:
        stock = ast.literal_eval(sf.read())
    with open(queueFile, 'r') as sf:
        queue = ast.literal_eval(sf.read())

    personFed = set()   # A set to store all the person who are already fed once
    personUnFed = set() # A set to store all the person who are left unfed
    for person in queue:
        print('{:-^160}'.format(""))
        if person[0] in personFed:  # check if person has been fed before
            print("{} have been sent to the brig.".format(person[0]))
        else:
            if stock.get(person[1], None):
                stock[person[1]] -= 1
                personFed.add(person[0])    # Register person as fed
                print("{} has been fed their food type {}".format(person[0],
                                                                  person[1]))
            else:
                personUnFed.add(person[0])
                print("{} has not been fed their food type {}".format(person[0],
                                                                      person[1]))
    print('{:=^160}'.format(""))
    print("Remaining stock are:")
    print(stock)
    print('{:=^160}'.format(""))
    print("People sent to the brig are:")
    print(', '.join(personFed))
    print('{:=^160}'.format(""))
    print("People left unfed are:")
    print(', '.join(personUnFed) if personUnFed else "None")

    # Writing updated stock to stockFile
    with open(stockFile, 'w') as sf:
        sf.write(str(stock))


def main():
    manageInventory()

if __name__ == "__main__":
    main()