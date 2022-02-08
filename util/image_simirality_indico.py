import math
import os
from random import sample
import re
import _pickle as pickle
from scipy import spatial
from PIL import Image
import numpy as np
import indicoio

def make_feats(paths):
    return indicoio.image_features(paths, batch=True, v=3)
def make_paths_list():
    with open("experiments/dataset_path.txt", mode='r') as f:
    # with open("experiments/mini_data.txt") as f:
        dir_pathes = [s.strip() for s in f.readlines()]
    photo_names =  []
    for dir_path in dir_pathes:
        photo_name = dir_path.replace("\\", "/")
        photo_name = re.search(r"\d-\d/\d*_\d*", photo_name).group() + ".jpg"
        photo_names.append(photo_name)
    return photo_names[:50]
def run():
    paths = make_paths_list()
    feats = make_feats(paths)
run()