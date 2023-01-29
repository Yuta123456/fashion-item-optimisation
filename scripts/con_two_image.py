
import glob
import sys
sys.path.append("D:\\fashion\\optimisation\\")
from constants.optimisation import LAYER
import numpy as np
import cv2
import random
def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)



dir_names = glob.glob('closet_images/select_two_comp/**')
for dir_name in dir_names:
    image_paths = glob.glob(dir_name + "/*.jpg")
    if len(image_paths) != 2:
        print("error!")
        exit()
    dir_name = dir_name.replace("\\", "/")

    image_paths = [i_p.replace("\\", "/") for i_p in image_paths]

    # randomに入れ替える
    random.shuffle(image_paths)
    paddingW = np.full((512,200, 3), 255, dtype=np.uint8)

    images_lists = []

    for image_path in image_paths:
        image = cv2.imread(image_path)
        images_lists.append(image)
        images_lists.append(paddingW)
    images_lists = images_lists[:-1]
    im_tile_resize = hconcat_resize_min(images_lists)
    print(dir_name)
    cv2.imwrite('comp_images/' + dir_name[len("closet_images/"):] + '.jpg', im_tile_resize)