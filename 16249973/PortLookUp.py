# -*- coding: utf-8 -*-

"""
- Tushar Gautam

- April 17, 2016

- The challenge is obtaining the a list of port numbers and converting that
  text based list into a python dictionary.

"""

from os.path import isfile, expanduser  # Python Standard Library OS Module

def CreatePortDictionary(portTextFile):
    """
    Parse the given file creating a Python dictionary named "portDictionary"
    :param portTextFile:
        Path for text file containing port data
    :returns:
        A dictionary "portDictionary" 
    """
    # Check if the portTextFile exists ptherwise raise an exception
    if not isfile(expanduser(portTextFile)): 
        raise Exception('The {} file does not exists'.format(portTextFile))
    
    portDict = {}   # An empty portDictionary
    with open(portTextFile, 'rb') as fp:
        for line in fp:
            lineList = line.split()
            # Now that each line must have a minimum of three parts.
            # Protocol, PortNumber and a Description to be valid
            if not len(lineList) >= 3:
                continue

            # A tuple (port, protocol)
            key = (lineList[1], lineList[0])
            # Port descriptions
            value = lineList[2:]
            portDict[key] = value

    return portDict

def PortLookup(portNumber, portDictionary):
    """
    Use dictionary to lookup and return the 
    tcpPortDescription and the udpPortDescription
    :param portNumber:
        The port number
    :param portDictionary:
        The portDictionary created after parsing portTextFile
    :returns:
        A tuple  tcpPortDescription, udpPortDescription
        and "unassigned" if key doesn't exists
    """
    # Fetch value from portDictionary with (given portNumber,protocol) as key
    # If the key doesn't exist then store "unassigned" to tcpPortDescription
    # and udpPortDescription.
    tcpPortDescription = portDictionary.get( (portNumber,"TCP"), "unassigned")
    udpPortDescription = portDictionary.get( (portNumber,"UDP"), "unassigned")

    return tcpPortDescription, udpPortDescription

def main():
    # Get portList file from user and pass as an argument to 
    # CreatePortDictionary. Store the returned value in portDict
    portTextFile = raw_input("Provide portList file: ")
    portDict = CreatePortDictionary(portTextFile)
    
    # Print neat table to display the data using format spec
    # Refer: https://docs.python.org/3/library/string.html#formatspec
    
    # Print table heading
    # '<' is for printing table left aligned
    # '>' is for printing table right aligned
    # '^' is for printing table center aligned
    # Currently, it prints left algined which looks good. But you can change
    # this by replacing the corresponding characters.
    print '+{:<50}| {:<50}  | {:<50}+'.format("Port",
                                              "TCP description",
                                              "UDP description")
    print '{:=^160}'.format("")
    
    # Print table body
    with open(portTextFile, 'rb') as fp:
        for line in fp:
            lineList = line.split()
            # Skip invalid lines
            if not len(lineList) >= 3:
                continue
            tcpPortDesc, udpPortDesc = PortLookup(lineList[1], portDict)
            print '{:<50}'.format(lineList[1]),
            # Check if value of tcpPortDesc is a string 'unassigned' 
            # or a list of string like ['PCMail,Server'] etc.
            if isinstance(tcpPortDesc,str):
                print '|  {:<50}'.format(tcpPortDesc),
            else:
                print '|  {:<50}'.format(','.join(tcpPortDesc)),
            # Check if value of udpPortDesc is a string 'unassigned' 
            # or a list of string like ['PCMail,Server'] etc.
            if isinstance(udpPortDesc,str):
                print '|  {:<50}'.format(udpPortDesc)
            else:
                print '|  {:<50}'.format(','.join(udpPortDesc))

if __name__ == "__main__":
    main()
