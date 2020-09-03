import os
import re
import csv

__name__ = "dataset_status"

def analyze_dataset(path):
	number_of_dirs = 0
	number_of_files = 0
	csv_dict = {'DATASET':path,'NUMBER_OF_CLASSES':0, 'TOTAL_NUMBER_OF_FILES':0}

	for base, dirs, files in os.walk(path):
		for directories in dirs:
			number_of_dirs += 1
			dir_path = os.path.join(path,directories)
			count = len(os.listdir(dir_path))
			csv_dict[str(directories)]= count
		for Files in files:
			number_of_files += 1

	csv_dict['NUMBER_OF_CLASSES'] = number_of_dirs
	csv_dict['TOTAL_NUMBER_OF_FILES'] = number_of_files

	with open('{path}/{path}.csv'.format(path=path), 'w') as f:
		for key in csv_dict.keys():
			f.write("%s,%s\n"%(key,csv_dict[key]))

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

#TODO implement natural sort to classes
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]