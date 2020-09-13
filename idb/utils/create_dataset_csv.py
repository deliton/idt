import os
import re
import csv
import yaml

__name__ = "create_dataset_csv"

def create_dataset_csv(path):
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

#TODO implement natural sort to classes
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def generate_class_info(dict, root_folder, folder):
	f = open(f"./{root_folder}/{folder}.yaml", "w")
	f.write(yaml.dump(dict))
