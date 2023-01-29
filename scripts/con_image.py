import glob
import sys
sys.path.append("D:\\fashion\\optimisation\\")
from constants.optimisation import LAYER
import numpy as np
from util.load_closet import load_closet
import cv2

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)
def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)


closet_names = glob.glob('closet/select_two_comp/**/*')
for closet_name in closet_names:
    closet_name = closet_name.replace("\\", "/")
    closet_name = closet_name[7:]
    closet = load_closet(closet_name)

    paddingW = np.full((512,20, 3), 255, dtype=np.uint8)
    paddingH = np.full((20, 1024, 3), 255, dtype=np.uint8)

    images_lists = [[] for i in range(LAYER+3)]

    p = 0
    for layer in range(LAYER):
        for item in closet[layer]:
            image = cv2.imread(item.get_image_path())
            images_lists[layer + p].append(image)
            images_lists[layer + p].append(paddingW)
        images_lists[layer + p + 1] = [paddingH]
        p += 1
    im_tile_resize = concat_tile_resize(images_lists)
    cv2.imwrite('closet_images/' + closet_name + '.jpg', im_tile_resize)
