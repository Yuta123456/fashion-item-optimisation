from os import close
import sys
sys.path.append("D:\\fashion\\optimisation\\")
from constants.optimisation import LAYER

from util.load_closet import load_closet
import cv2
args = sys.argv
try: 
    closet_name = args[1]
    image_name = args[2]
except IndexError as e: 
    # 引数が足りないことを示す
    raise Exception("引数が足りません.")

closet = load_closet(closet_name)
# 画像の読み込み
# im1 = cv2.imread('data/src/lena.jpg')
# im2 = cv2.imread('data/src/rocket.jpg')
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

images_lists = [[] for i in range(LAYER)]
for layer in range(LAYER):
    for item in closet[layer]:
        image = cv2.imread(item.get_image_path())
        images_lists[layer].append(image)
im_tile_resize = concat_tile_resize(images_lists)
cv2.imwrite('closet_images/' + image_name + '.jpg', im_tile_resize)