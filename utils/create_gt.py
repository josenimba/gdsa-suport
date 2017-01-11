import numpy as np
import os
import sys, time
import glob
import random
import shutil

"""
This will create annotation files for the dataset in params['image_dir'].
It will create a new dataset folder with all images together and txt files
with annotations

Usage:
python create_gt.py path_to_image_dir path_to_save_dir

(running with default params is also possible)
"""

def get_params():
    params = {}

    # Directories
    params['root'] = '/imatge/asalvador/'
    params['image_dir'] = "/work/gdsa-projecte/raw"
    params['workspace'] = "/imatge/asalvador/workspace/teaching/gdsa/teachers/utils"
    params['save_dir'] = "/work/gdsa-projecte/TerrassaBuildings900"

    # Splitting parameters

    params['train_split'] = 0.5
    params['val_split'] = 0.2
    params['test_split'] = 0.3

    return params

def setup(params):

    os.getcwd()
    os.chdir(params['workspace'])

    print "Working directory set to:", os.getcwd()

def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def split_class(params,class_elements):

    train_split = class_elements[0:int(params['train_split']*len(class_elements))]
    val_split = class_elements[int(params['train_split']*len(class_elements)):int(params['train_split']*len(class_elements)) + int(params['val_split']*len(class_elements)) ]
    test_split = class_elements[int(params['train_split']*len(class_elements)) + int(params['val_split']*len(class_elements)):]

    return train_split, val_split, test_split

def save_txt(params,names,labels,partition):

     # Remove extensions
    f = lambda x: x.split('.')[0]
    names = map(f, names)

    file = open(os.path.join(params['save_dir'],partition, 'annotation.txt'), "w")

    file.write("ImageID" + "\t" + "ClassID" + "\n")

    for index in range(len(names)):
        file.write(str(names[index]) + "\t" + str(labels[index]) + "\n")
    file.close()

def move_files(params,names,c,partition):
    # actually not moving but copying cause you never know
    makedir(os.path.join(params['save_dir'], partition))
    makedir(os.path.join(params['save_dir'], partition, 'images'))
    for name in names:

        shutil.copy(os.path.join(params['image_dir'],c,name), os.path.join(params['save_dir'], partition, 'images',name))

def save_annotations(params):

    # Initialize lists to be filled
    train = []
    val = []
    test = []

    label_train = []
    label_val = []
    label_test = []

    # Get class names as directories
    classes = os.listdir(params['image_dir'])
    makedir(params['save_dir'])
    for c in classes:

        # Get image names in this class
        class_elements = os.listdir(os.path.join(params['image_dir'], c))

        # Sort them randomly
        random.shuffle(class_elements)

        # Split
        train_split, val_split, test_split = split_class(params,class_elements)

        # Some info...
        print "Class name is:", c
        print "Number of elements is", len(class_elements)
        print "Partitions:"
        print "train:",len(train_split), "val:", len(val_split), "test:", len(test_split), "total:", len(train_split) + len(val_split) + len(test_split)
        print "="*10
        # Move files to partition directories

        move_files(params,train_split,c,'train')
        move_files(params,val_split,c,'val')
        move_files(params,test_split,c,'test')

        # Add to the partition lists
        train.extend(train_split)
        val.extend(val_split)
        test.extend(test_split)

        # Keep their labels

        label_train.extend([c]*len(train_split))
        label_val.extend([c]*len(val_split))
        label_test.extend([c]*len(test_split))


    print "============ "

    print "Saving annotations..."

    save_txt(params,train,label_train,'train')
    save_txt(params,val,label_val,'val')
    save_txt(params,test,label_test,'test')

    print "Done."


if __name__ == "__main__":

    params = get_params()

    if len(sys.argv)>1:
        params['image_dir'] = sys.argv[1]
        params['save_dir'] = sys.argv[2]
    #setup(params)
    save_annotations(params)
