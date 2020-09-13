import os
import random
from shutil import copyfile

__name__ = "split_dataset"

def split_dataset(img_source_dir, train_size):
    train_size = float(train_size / 100)

    print("Creating a dataset split into train/validation folders...")

    if not os.path.exists(img_source_dir):
        raise OSError('The source folder doesnt exist. Are you sure the dataset folder is ', img_source_dir)
        
    # Create folders
    if not os.path.exists('split-dataset'):
        os.makedirs('split-dataset')
    else:
        if not os.path.exists('split-dataset/train'):
            os.makedirs('split-dataset/train')
        if not os.path.exists('split-dataset/validation'):
            os.makedirs('split-dataset/validation')
            
    # Get the subdirectories in the main image folder
    subdirs = [subdir for subdir in os.listdir(img_source_dir) if os.path.isdir(os.path.join(img_source_dir, subdir))]

    for subdir in subdirs:
        subdir_fullpath = os.path.join(img_source_dir, subdir)
        if len(os.listdir(subdir_fullpath)) == 0:
            print(subdir_fullpath + ' is empty')
            break

        train_subdir = os.path.join('split-dataset/train', subdir)
        validation_subdir = os.path.join('split-dataset/validation', subdir)

        # Create subdirectories in train and validation folders
        if not os.path.exists(train_subdir):
            os.makedirs(train_subdir)

        if not os.path.exists(validation_subdir):
            os.makedirs(validation_subdir)

        train_counter = 0
        validation_counter = 0

        # Randomly assign an image to train or validation folder
        for filename in os.listdir(subdir_fullpath):
            if filename.endswith(".jpg") or filename.endswith(".png"): 
                fileparts = filename.split('.')

                if random.uniform(0, 1) <= train_size:
                    copyfile(os.path.join(subdir_fullpath, filename), os.path.join(train_subdir, str(train_counter) + '.' + fileparts[1]))
                    train_counter += 1
                else:
                    copyfile(os.path.join(subdir_fullpath, filename), os.path.join(validation_subdir, str(validation_counter) + '.' + fileparts[1]))
                    validation_counter += 1