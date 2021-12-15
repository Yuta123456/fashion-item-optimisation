import glob
import os
from PIL import Image
import uuid
from constants.optimisation import USER_GENDER, Gender
from util_class.FashionItem import FashionItem
import re

def init_all_item(LAYER, LAYER_NAME, length):
    photo2gender = {}

    with open("../images/RichWear/photos.txt") as f:
        photos = [s.strip() for s in f.readlines()]
    with open("../images/RichWear/gender.txt") as f:
        genders = [s.strip() for s in f.readlines()]
    print(photos[:10])

    for i in range(len(photos)):
        photo2gender[photos[i]] = genders[i]
    all_item = [[] for i in range(LAYER)]
    dir_pathes = glob.glob('../images/RichWearImageSprited/**/**/')[:length]
    for dir_path in dir_pathes:
        photo_name = dir_path.replace("\\", "/")
        photo_name = re.search(r"\d-\d/\d*_\d*", photo_name).group() + ".jpg"
        # ディレクトリを見て、男か女か判断する。
        gender = photo2gender[photo_name]
        if Gender(gender) != USER_GENDER :
            continue
        for layer in range(LAYER):
            layer_name = LAYER_NAME[layer]
            image_path = dir_path + f"{layer_name}.jpg"
            if os.path.exists(image_path):
                image_path = dir_path + f"{layer_name}.jpg"
            else:
                continue
            with open(dir_path + "attribute2.txt") as f:
                # 該当するレイヤーのアイテムだけ取得
                attribute = [s.strip() for s in f.readlines() if s.startswith(layer_name)]
                attribute = list(set(attribute))
            id = uuid.uuid4()
            if len(attribute) == 0:
                continue
            item = FashionItem(image_path, layer, attribute, id)
            all_item[layer].append(item)
    return all_item