'''
Title   : Team C Submission for Major Assignment 1
Date    : 25 April 2016
Class   : DFS-510-85
Members : Kyle Anderson
          Gregg Bennett
      Christiana Brewer
      Samuel Brothers
      Todd Haymore
      John Johnson
'''
'''
Copyright (c) 2014 Chet Hosmer

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

'''

import os           # Python Standard Library OS Module
import time         # Python Standard Library Time Module
import hashlib      # Python Standard Library Hashing Methods
import logging      # Python Standard Library - Logging ***SB***

# Class: FileExaminer Class
#
# Desc: Handles all methods related to File Based Forensics
# Methods  constructor:    Initializes the Forensic File Object
#                          and Collects Basic Attributes
#                          File Size
#                          MAC Times
#                          Reads file into a buffer
#          hashFile:       Generates the selected one-way hash of the file
#          destructor:     Deletes the Forensic File Object


class FileExaminer:

    # get logging object from main program
    # this will ensure that all log messages
    # are written to the same log file

    log = logging.getLogger('main._pfish')

    # Constructor

    def __init__(self, theFile):

        # Attributes of the Object

        self.lastError = "OK"
        self.mactimes = ["", "", ""]
        self.fileSize = 0
        self.fileType = "unknown"
        self.uid = 0
        self.gid = 0
        self.mountPoint = False
        self.fileRead   = False
        self.md5        = ""
        self.sha1       = ""

        try:

            if os.path.exists(theFile):
                # get the file statistics
                theFileStat = os.stat(theFile)

                # get the MAC Times and store them in a list

                self.macTimes = []
                self.macTimes.append(time.ctime(theFileStat.st_mtime))
                self.macTimes.append(time.ctime(theFileStat.st_atime))
                self.macTimes.append(time.ctime(theFileStat.st_ctime))

                # get and store the File size

                self.fileSize = theFileStat.st_size

                # Get and store the ownership information

                self.uid = theFileStat.st_uid
                self.gid = theFileStat.st_gid

                if os.path.isfile(theFile):
                    self.fileType = "File"
                # Is this a real file?
                elif os.path.islink(theFile):
                    self.fileType = "Link"
                # Is This filename actually a directory?
                elif os.path.isdir(theFile):
                    self.fileType = "Directory"
                else:
                    self.fileType = "Unknown"

                # Is the pathname a mount point?
                if os.path.ismount(theFile):
                    self.mountPoint = True
                else:
                    self.mountPoint = False

                # Is the file Accessible for Read?

                if os.access(theFile, os.R_OK) and self.fileType == "File":

                    # Improved file I/O added by tushar_rishav
                    # Open the file
                    with open(theFile, 'rb') as fp:
                        # Assume we have enough space
                        self.buffer = fp.read()
                        # Close the file we have the entire file in memory
                        # File gets closed automatically once execution leaves
                        # this block. Hence, no need to explicitly close
                        # the file using fp.close()
                        # Recommended way for handling file I/O : Refer PEP343

                    self.fileRead = True

                else:
                    self.fileRead = False

            else:
                self.lastError = "File does not exist"

        except:
            self.lastError = "File Exception Raised"

    # partially completed hash file method

    def hashFile(self, hashType):

        # --------------------------------------------------
        # AIM : Add hash types for SHA224, SHA512, etc.
        # STATUS: Accomplished
        # AUTHOR: tushar_rishav
        # --------------------------------------------------
        try:

            if hashType == "MD5":
                hashObj = hashlib.md5()
                hashObj.update(self.buffer)
                self.md5 = hashObj.hexdigest().upper()
                self.lastError = "OK"
                return True
            elif hashType == "SHA1":
                hashObj = hashlib.sha1()
                hashObj.update(self.buffer)
                self.sha1 = hashObj.hexdigest().upper()
                self.lastError = "OK"
                return True
                # Ability to hash data using SHA256 algorithm - Added By Sam
                # Brothers on 4/4/16
            elif hashType == "SHA256":
                # Performs the SHA-256 function over the data from
                # hashObj
                hashObj = hashlib.sha256()
                hashObj.update(self.buffer)
                # Converts all letters in the hash to all capitols.
                self.sha256 = hashObj.hexdigest().upper()
                self.lastError = "OK"
                return True
            # SHA384 added by Team C
            elif hashType == "SHA384":
                hashObj = hashlib.sha384()
                hashObj.update(self.buffer)
                self.sha384 = hashObj.hexdigest().upper()
                self.lastError = "OK"
                return True
            # SHA224 added by tushar_rishav
            elif hashType == "SHA224":
                hashObj = hashlib.sha224()
                hashObj.update(self.buffer)
                self.sha224 = hashObj.hexdigest().upper()
                self.lastError = "OK"
                return True
            # SHA512 added by tushar_rishav
            elif hashType == "SHA512":
                hashObj = hashlib.sha512()
                hashObj.update(self.buffer)
                self.sha512 = hashObj.hexdigest().upper()
                self.lastError = "OK"
                return True
            else:
                self.lastError = "Invalid Hash Type Specified"
                return False
        except:
            self.lastError = "File Hash Failure"
            return False

    def hashAll(self):
        # --------------------------------------------------
        # AIM: Write a code to call all the hash types in hashFile()
        # STATUS: Accomplished
        # AUTHOR: tushar_rishav
        # --------------------------------------------------

        # Create a set to automate the calling of hashFile method
        # on each hash types.
        hash_set = {"SHA1", "SHA224", "SHA256", "SHA384", "SHA512", "MD5"}
        if self.fileRead:
            for hash_type in hash_set:
                if self.hashFile(hash_type):
                    # use `getattr` to get a named attribute from an object;
                    # getattr(obj, attr) is equivalent to obj.attr
                    # For example: getattr(self, 'sha1') -> self.sha1
                    print "{}: {}".format(hash_type, getattr(self,
                                                             hash_type.lower()))
                    # Prints "sha1: 6EA656893EF7D5E3060E560F58EDC6D8".
                    # Similarly for each of the hash types
                else:
                    print self.lastError
        del self

    def __del__(self):
        print "closed"

# End Forensic File Class ====================================

#
# ------ MAIN SCRIPT STARTS HERE -----------------
#

if __name__ == '__main__':

    # a forensic file object

    print "File Examainer Object Test \n"

    # --------------------------------------------------
    # AIM: Take command line input from user
    # STATUS: Accomplished
    # AUTHOR: tushar_rishav
    # --------------------------------------------------

    FEobj = FileExaminer(raw_input("Provide the File path"))

    if FEobj.lastError == "OK":

        print "MAC  Times: {}".format(FEobj.macTimes)
        print "File  Size: {}".format(FEobj.fileSize)
        print "Owner ID:   {}".format(FEobj.uid)
        print "Group ID:   {}".format(FEobj.gid)
        print "File  Type: {}".format(FEobj.fileType)
        print "Mount Point:{}".format(FEobj.mountPoint)
        print "File Read:  {}".format(FEobj.fileRead)

        # --------------------------------------------------
        # AIM: Call to hashAll function:
        # STATUS: Accomplished
        # AUTHOR: tushar_rishav
        # --------------------------------------------------

        FEobj.hashAll()

    else:
        print "Last Error: ", FEobj.lastError
