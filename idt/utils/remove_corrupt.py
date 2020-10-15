import os, hashlib, re, csv

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

def erase_duplicates(folder):
	duplicates = []
	hash_keys = dict()
	file_list = os.listdir(folder)

	for index, file_name in enumerate(file_list):
		if os.path.isfile(os.path.join(folder,file_name)):
			with open(os.path.join(folder,file_name), 'rb') as f:
				filehash = hashlib.md5(f.read()).hexdigest()
			if filehash not in hash_keys:
				hash_keys[filehash] = index
			else:
				duplicates.append((index, hash_keys[filehash]))
				
	for index in duplicates:
		os.remove(os.path.join(folder, file_list[index[0]]))

	return len(duplicates)