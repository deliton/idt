import os
import re
import csv

__name__ = "remove_corrupt"

def remove_corrupt(path):
	visited_dir = 0
	print("Removing corrupt files")

	for base, dirs, files in os.walk(path):
		for directories in dirs:
			visited_dir += 1
		for Files in files:
			file = os.path.join(base,Files)
			if os.stat(file).st_size == 0:
				#print(Files, "is corrupt, removing it...")
				os.remove(file)
