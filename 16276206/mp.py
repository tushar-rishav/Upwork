"""
Author:
	John T.
Date: 
	2016/04/22
Description:
	Multiprocessing script using the examples in Chapter 10 & 11 as a guide. 
	The challenge problem is the following:
	1. Develop a script that will simultaneously
	a. Hash an input file
	b. Search the same input file for possible phone numbers using a regular expression
	2. Separate processing into two cores
	Core 1: Hashing
	Core 2: Search
	3. Time the results of each along with the total time to complete both.


"""

import hashlib 	# Python hashing module
import multiprocessing # Python multiprocessing module
import os
import re # Python regex module
import sys
import time # Python Time module

def hash_of_file(file_name):
	"""
	Create and print a hash of a given file's content.
	:params file_name:
		Name of the file that's to be hashed
	"""
	try:
		hasher=hashlib.sha256()
		with open(file_name, 'rb') as fp:
			hasher.update(fp.read())
			print(file_name,hasher.hexdigest())
		del hasher
	except Exception as e:
		print(e)
		sys.exit(0)

def search_phone_in_file(file_name):
	"""
	Search the given file for possible phone numbers using
	regular expressions.
	:params file_name:
		Name of the file that's to be hashed
	"""
	# Create regex for phone number patter.
	# Tested at https://regex101.com/
	phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
	print("Possible phone numbers found are: ")
	with open(file_name, 'r') as fp:
		for line in fp:
			# Search for phone numbers line by line
			match = phonePattern.search(line)
			print('-'.join(match.groups()) if match else None)

def main():
	file_name = raw_input(">Enter the file path: ")
	# Proceed only if we have multi core system
	if multiprocessing.cpu_count() < 2:
		print("multiprocessing can't be used here. CPU core is less than 2")
		sys.exit(0)

	# Create a pool of processes
	corePool = multiprocessing.Pool(processes=2)
	# Start the timer
	startTime = time.time()
	# Map each process to cores and call the function to be executed
	hash_result = corePool.map(hash_of_file, (file_name,))
	# Note the hashing time
	hash_time = time.time() - startTime
	print("Time taken to hash file contents: {} seconds".format(hash_time))
	search_result = corePool.map(search_phone_in_file, (file_name,))
	# Note the search time
	search_time = time.time() - startTime
	print("Time taken to search phone numbers in file: {} seconds".format(search_time))
	print("Total time taken: {} seconds".format(hash_time + search_time))

if __name__ == "__main__":
	main()
