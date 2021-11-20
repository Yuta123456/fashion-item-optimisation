import glob
import os
from PIL import Image
import uuid
from util_class.FashionItem import FashionItem
def init_all_item(LAYER, LAYER_NAME, length):
    all_item = [[] for i in range(LAYER)]
    dir_pathes = glob.glob('../images/RichWearImageSprited/**/**/')[:length]
    for dir_path in dir_pathes:
        for layer in range(LAYER):
            layer_name = LAYER_NAME[layer]
            image_path = dir_path + f"{layer_name}.jpg"
            if os.path.exists(image_path):
                image_path = dir_path + f"{layer_name}.jpg"
            else:
                continue
            with open(dir_path + "attribute.txt") as f:
                # 該当するレイヤーのアイテムだけ取得
                attribute = [s.strip() for s in f.readlines() if s.startswith(layer_name)]
                attribute = list(set(attribute))
            id = uuid.uuid4()
            if len(attribute) == 0:
                continue
            item = FashionItem(image_path, layer, attribute, id)
            all_item[layer].append(item)
    return all_item